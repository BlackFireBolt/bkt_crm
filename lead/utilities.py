import channels.layers
from asgiref.sync import async_to_sync
import logging
import json

logger = logging.getLogger(__name__)


def broadcast(user, content):
    # Add condition if user has subscribed in Redis
    channel_layer = channels.layers.get_channel_layer()
    logger.info("sending socket to : " + 'realtime_' + str(user))
    logger.info("Content : " + str(content))
    async_to_sync(channel_layer.group_send)(
        '{}'.format(user), {
            "type": 'data_send',
            "content": json.dumps(content),
        })
