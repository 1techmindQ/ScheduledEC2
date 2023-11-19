import boto3
import datetime
import logging
import pytz

# Create a session and EC2 resource using AWS profile in the us-east-1 region
aws_gui = boto3.session.Session(profile_name="")
ec2_gui = aws_gui.resource(service_name="ec2", region_name="us-east-1")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def manage_specific_instance(instance_id):
    # Get the current time in EST
    eastern = pytz.timezone('US/Eastern')
    current_time = datetime.datetime.now(eastern).time()
    current_day = datetime.datetime.now(eastern).weekday()  # Get the current day (0 - Monday, 6 - Sunday)

    # Define start and stop times in EST
    start_time = datetime.time(8, 0, 0)  # Set the start time to 8:00 AM EST
    stop_time = datetime.time(18, 0, 0)  # Set the stop time to 6:00 PM EST

    # Check if it's a weekday (Monday to Friday) and within the scheduled time
    if 0 <= current_day <= 4:  # 0 - Monday, 4 - Friday
        if start_time <= current_time <= stop_time:
            instance = ec2_gui.Instance(instance_id)
            state = instance.state['Name']

            if state == 'stopped':
                instance.start()
                print(f"Started instance: {instance_id}")
        else:
            instance = ec2_gui.Instance(instance_id)
            state = instance.state['Name']

            if state == 'running':
                instance.stop()
                print(f"Stopped instance: {instance_id}")
    else:
        print("Outside of scheduled time.")

# Replace 'YOUR_INSTANCE_ID' with your specific instance ID
specific_instance_id = ''
manage_specific_instance(specific_instance_id)  # Call the function to manage the specific EC2 instance
