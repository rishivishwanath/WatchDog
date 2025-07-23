import json
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

def create_topics_from_json(json_path, bootstrap_servers='localhost:9092'):
    # Load JSON file
    with open(json_path) as f:
        topics_data = json.load(f)

    # Initialize Kafka Admin Client
    admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers, client_id='topic-creator')

    # Convert to NewTopic objects
    topic_list = [
        NewTopic(name=topic["name"], num_partitions=topic["partitions"], replication_factor=topic["replication_factor"])
        for topic in topics_data
    ]

    # Create topics
    try:
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
        print("Topics created successfully.")
    except TopicAlreadyExistsError as e:
        print("Some topics already exist.")
    finally:
        admin_client.close()

if __name__ == "__main__":
    create_topics_from_json("topics.json")
