from py2neo import Graph, Database, Node, Relationship
from tqdm import tqdm


class GraphBuilder:

    def __init__(self, twitter_user, username, password, hostname, port):
        """
        Initialize the DB and create the Ego node.

        :param twitter_user: accept a TwitterUser object
        """
        self.username = username
        self.password = password
        self.uri = f'bolt://{hostname}:{port}'

        self.db = Database(self.uri, auth=(self.username, self.password))
        self.g = Graph()
        self.twtr_user = twitter_user
        self.ego = Node('Ego', name=self.twtr_user.name)
        self.g.create(self.ego)

    def run_query(self, query):
        """
        Make queries with Cypher.

        :param query: Cypher query as a str
        :return: return result of given query
        """
        return self.g.run(query).data()[0]

    def build(self, obj):
        """
        Populate DB with 'is_following' or 'followed_by' relationships.

        :param obj: which relationships to build - accept 'following' or 'followers'
        """

        if obj == 'following':
            rel = Relationship.type('is_following')

            for p in tqdm(self.twtr_user.following,
                          desc='Building following relationships'):
                person = Node('Following', name=p['name'])

                self.g.merge(rel(self.ego, person), 'Following', 'name')

        if obj == 'followers':
            rel = Relationship.type('followed_by')

            for p in tqdm(self.twtr_user.followers,
                          desc='Building followers relationships'):
                person = Node('Follower', name=p['name'])

                self.g.merge(rel(self.ego, person), 'Follower', 'name')
