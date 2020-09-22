# Matchy

# Imports
import slack
import json
from random import randrange
import config


# Intro message that gets sent to groups
# Put `%s` wherever you'd like the usernames to appear
intro_message = '''
_Wing, wing_ :telephone_receiver: 
Hey %s! 
You have been matched this week :hatching_chick:
Go ahead and figure out _wren_ (when) you're both free to meet up for a virtual meeting :smile:
'''


# Global Variables
match_channel = config.CHANNEL      # Channel that the pairs come from (#bot-playground)
partners_file = "partners.json"     # JSON file that contains previous partners

# Slack Client
slack_client = slack.WebClient(config.OAUTH_TOKEN)


# Load Previous Partners
#   Loads the JSON from `partners_file` into a dict. 
#   If the file doesn't exist, it will return an empty dict.
#
#   Returns 
#       Dict {str: [str]} where the strings are user IDs
def load_previous_partners() -> dict:
    # Attempt to open the partners_file
    try:
        # If it exists, return the json object
        with open(partners_file) as json_file:
            return json.load(json_file)
    except:
        # If it doesn't exist, return an empty dict
        return dict()

# Save Partners
#   Given the new pairs and the previous partners, this computes a new JSON for
#   previous partner pairs and saves it to the partner_file.
#
#   Params
#       new_pairs: [[str, str]]             - List of pairs
#       previous_partners: {str: [str]}     - Previous partners loaded from file
#
#   Post
#       Overwrites the partner_file to be the updated JSON
def save_partners(new_pairs: [[str, str]], previous_partners: {str: [str]}):
    # Iterate over each pair and add every partner to the prev partners dict
    for pair in new_pairs:
        for user in pair:
            for partner in pair:
                # Since we iterate over pair twice, we have to ignore the
                # the iteration where user == partner
                if not user == partner:
                    # Add the new partner to the previous_partners
                    if user in previous_partners:
                        previous_partners[user].append(partner)
                    else:
                        previous_partners[user] = [partner]

    # Write the updated json to partners_file
    with open(partners_file, 'w') as json_file:
        json.dump(previous_partners, json_file)    


# Get Channel Members
#   Given the name of a channel, retrieve the list of users in that channel.
#
#   Params
#       channel: str    - channel name
#
#   Returns 
#       List of slack ids for the users in the channel
def get_channel_members(channel: str) -> [str]:
    api_call = slack_client.conversations_members(channel = channel)
    users_id = api_call["members"]
    return users_id

# Generate Pairs
#   Given a list of users and their previous partners, generate pairs or users.
#   Preferably, users wouldn't be paired with recent partners.
#   If len(users) is odd, there will be one group of three.
#
#   Params
#       users: [str]                        - list of users to be paired
#       previous_partners: {str: [str]}     - Previous partners for each user
#
#   Returns
#       List of pairs of users [[str, str]]
def generate_pairs(users: [str], previous_partners: {str: [str]}) -> [[str, str]]:
    pairs = []
    is_odd = len(users)%2 == 1
    
    # The pairing algorithm only works with an even number of people.
    # So if there are an odd number of people, we need to remove one
    # and randomly assign them to a group of three at the end.
    if is_odd:
        odd_one_out = users.pop(randrange(len(users)))
        
    # Loop until there are no more unpaired users
    while users:
        # Get a random user from the list
        user = users.pop(randrange(len(users)))
        pulled_users = set()
        
        # Continue searching for a partner is found
        while True:
            # Pull a random partner from users
            partner = users.pop(randrange(len(users)))
            
            # See if this user has had any prev partners
            if not user in previous_partners:
                break

            # See if this partner was a prev partner
            elif not partner in previous_partners[user]:
                break
            
            # Give up if there are no remaining potential partners
            elif len(users) == 0:
                #TODO: pick least recently paired user from pulled_users
                break
            
            # Otherwise toss them aside and keep searching
            else:
                pulled_users.add(partner)

        # Add the new pair to pairs
        pairs.append([user,partner])

        # Put the previous partners back into users
        users += list(pulled_users)

    # Randomly assign the odd one out to a group of three
    if is_odd:
        pairs[randrange(len(pairs))].append(odd_one_out)

    return pairs

# Create Group Chats
#   Given a list of users, create a new groupchat.
#
#   Params
#       users: [str]    - List of users to add to the groupchat
#
#   Post
#       A new groupchat with the users will be created in Slack
#       Returns the ID of the groupchat       
def create_group_chat(users: [str]) -> str:
    # Open a groupchat with all users in users
    api_call = slack_client.conversations_open(users = users)
    
    # Retrieve and return ID of the groupchat
    return api_call['channel']['id']

# Send Group Intro Message
#   Given a group ID, send the group an introduction message.
#
#   Params
#       group_id: str   - ID of the group to message
#       users: [str]    - List of users in the groupchat
#
#   Post
#       Sends a message to the group
def send_group_intro_message(group_id: str, users: [str]):
    # Post a message to the group
    response = slack_client.chat_postMessage(
        channel = group_id,
        text = intro_message % _generate_usernames(users)
    )

# Generate Usernames
#   Given a list of users, we need to format it for slack
#
#   Params
#       users: [str]    - List of user IDs
#
#   Returns
#       String with the format: "<@ID>, <@ID>"
def _generate_usernames(users: [str]) -> str:
    return "<@" + ">, <@".join(users) + ">"

if __name__ == "__main__":
    # Load previous partners from /logs
    previous_partners = load_previous_partners()

    # Get the users currently in the Slack channel
    channel_members = get_channel_members(match_channel)

    # Generate the new partner pairs
    new_pairs = generate_pairs(channel_members, previous_partners)

    # Save the new pairings to the JSON file
    save_partners(new_pairs, previous_partners)

    # Create a groupchat on Slack for each pair
    for pair in new_pairs:
        group_id = create_group_chat(pair)
        send_group_intro_message(group_id, pair)
        print(pair, group_id)
