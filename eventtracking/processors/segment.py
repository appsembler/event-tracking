"""Process events to be more useful with Segment backend"""

from __future__ import absolute_import

from eventtracking.processors.exceptions import EventEmissionExit


class SegmentTopLevelPropertiesProcessor(object):
    """

    Most Segment.io Destination APIs require properties to be at the top level
    of the event. Copy all properties contained within the event's 'data' key
    to the top level of the event dict.

    We duplicate instead of reassign to not break previous integrations.

    Always returns the event for continued processing.
    """

    def __call__(self, event):
        try:
            for key, val in event['data'].items():
                try:
                    event[key].update(event['data'][key])
                except (KeyError, AttributeError):
                    event[key] = val
        except KeyError:  # no data
            pass
        return event
