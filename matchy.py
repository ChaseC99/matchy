# Matchy

# Imports
import slack
import secrets

# Global Variables
match_channel ="C01AU7UCNGN"      # Channel that the pairs come from (#bot-playground)
partners_file = ""      # JSON file that contains previous partners

# Slack Client
slack_client = slack.WebClient(secrets.oauth_token)


# Load Previous Partners
#   Loads the JSON from `partners_file` into a dict. 
#   If the file doesn't exist, it will return an empty dict.
#
#   Returns 
#       Dict {str: [str]} where the strings are user IDs
def load_previous_partners() -> dict:
    return dict()

# Save Partners
#   Given the new pairs and the previous partners, this computes a new JSON for
#   previous partner pairs and saves it to the partner_file.
#
#   Params
#       new_pairs: [(str, str)]             - List of pairs
#       previous_partners: {str: [str]}     - Previous partners loaded from file
#
#   Post
#       Overwrites the partner_file to be the updated JSON
def save_partners(new_pairs: [(str, str)], previous_partners: {str: [str]}):
    return


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
    return users_id;

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
#       List of pairs of users [(str, str)]
def generate_pairs(users: [str], previous_partners: {str: [str]}) -> [(str, str)]:
    pairs = []
    if (len(users) % 2) == 0:   #even
        for user, partners in previous_partners.items():
            for available in users:
                if available not in partners:
                    pairs.append((user, available))
    
    else:   #odd
    # gotta fix this whelp
    return users

# Create Group Chats
#   Given a list of users, create a new groupchat.
#
#   Params
#       users: [str]    - List of users to add to the groupchat
#
#   Post
#       A new groupchat with the users will be created in Slack       
def create_group_chat(users: [str]):
    # Open a groupchat with all users in users
    api_call = slack_client.conversations_open(users = users)
    # Retrieve channel information
    channel_info = api_call['channel']

    try:
        # If the groupchat was made, post a message
        response = slack_client.chat_postMessage(
            channel = channel_info["id"],
            text = "Matchy here, meet your new partner and get to know them!" 
        )
    except SlackApiError as e:
        # If "ok" is False, assertion
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    return


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
    # for pair in new_pairs:
        # create_group_chat(pair)
    create_group_chat(new_pairs)    # for testing
