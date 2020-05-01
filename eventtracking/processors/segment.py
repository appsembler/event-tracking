"""Process events to be more useful with Segment backend"""


class SegmentTopLevelPropertiesProcessor(object):
    """

    Most Segment.io Destination APIs require properties to be at the top level
    of the event. Copy all properties contained within the event's 'data' key
    to the top level of the event dict.

    We copy properties instead of reassign to not break previous integrations.

    For example: by default, tracker.emit() will produce an event
    with most interesting properties in the `data` key, like:

    analytics.track('13', 'edx.bi.user.chapter.started', {
    'context': { ... },
    'data': {
        'block_id': 'block-v1:foo+101+forever+type@chapter+block@3707382f0c284b6aadbd7c50d767ca8f',
        'block_name': 'Section 1',
        'completion_percent': 33.3333333333333,
        'course_id': 'course-v1:foo+101+forever',
        'course_name': 'CompletionTest',
        'label': 'chapter Section 1 started'
    },
    'name': 'edx.bi.user.chapter.started',
    ...
    })

    Many/most Segment Destinations will not be able to access properties inside 'data'.
    Copy these to the top level of the event before emitting.

    Always returns the event for continued processing.
    """

    def __call__(self, event):
        try:
            for key, val in event['data'].items():
                if key in event:
                    try:
                        event[key].update(event['data'][key])  # dict
                    except AttributeError:
                        try:
                            event[key].extend(event['data'][key])  # list
                        except AttributeError:
                            event[key] = val
                else:
                    event[key] = val
        except KeyError:  # no 'data'
            pass
        return event
