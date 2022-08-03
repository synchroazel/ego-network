import argparse

from graph_builder import *
from twitter_user import *


def main(user, username, password, hostname, port):
    # create TwitterUser object for given username
    ego_user = TwitterUser(user)

    # create GraphBuilder object using ego_user as ego node
    graph_db = GraphBuilder(ego_user, username, password, hostname, port)

    q = '''
        MATCH (n)
        WHERE n:Following OR n:Follower
        RETURN count(n)
        '''

    # if the DB is not empty:
    if graph_db.run_query(q)['count(n)'] != 0:

        q = 'MATCH (n:Following) RETURN count(n) as count'

        # if count of 'Following' nodes is not the same as .following_count an update is needed
        if graph_db.run_query(q)['count'] != ego_user.following_count:
            print('The DB is not empty, but an update to \'following\' is needed.')

            ego_user.get('following', all=False, max_results=100)
            graph_db.build('following')

        q = 'MATCH (n:Follower) RETURN count(n) as count'

        # if count of 'Followers' nodes is not the same as .followers_count an update is needed
        if graph_db.run_query(q)['count'] != ego_user.followers_count:
            print('The DB is not empty, but an update to \'followers\' is needed.')

            ego_user.get('followers', all=False, max_results=100)
            graph_db.build('followers')

    # else, if DB is empty
    else:
        print('The DB is empty! Populating it right now ...')
        ego_user.get('following', all=False, max_results=100)
        graph_db.build('following')
        ego_user.get('followers', all=False, max_results=100)
        graph_db.build('followers')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Build a graph for a Twitter user given its username and the Neo4j credentials for the db')

    parser.add_argument('-t', '--twitter_user', type=str, help='username of the Twitter user to build the graph of')
    parser.add_argument('-u', '--username', type=str, default='neo4j', help='username to connect to Neo4j db')
    parser.add_argument('-w', '--password', type=str, default='password', help='password to connect to Neo4j db')
    parser.add_argument('-h', '--hostname', type=str, default='localhost', help='hostname to connect to Neo4j db')
    parser.add_argument('-p', '--port', type=int, default=7687, help='port to connect to Neo4j db')

    args = parser.parse_args()

    main(args.user, args.username, args.password, args.hostname, args.port)
