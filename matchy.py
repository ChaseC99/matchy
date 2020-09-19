# Matchy

# Imports
import slack
import secrets

# Global Variables
match_channel ="#"      # Channel that the pairs come from
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
    return []

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
    return []

# Create Group Chats
#   Given a list of users, create a new groupchat.
#
#   Params
#       users: [str]    - List of users to add to the groupchat
#
#   Post
#       A new groupchat with the users will be created in Slack       
def create_group_chat(users: [str]):
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
    for pair in new_pairs:
        create_group_chat(pair)

