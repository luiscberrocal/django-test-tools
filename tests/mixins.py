import json
import os


class TestFixtureMixin(object):

    def get_json_data(self, filename):
        import environ
        full_path = (environ.Path(__file__) - 1).root
        fixture_path = None
        max_levels = 4
        current_level = 1
        while fixture_path is None:
            new_path = '{}{}{}'.format(full_path, os.sep, 'fixtures')
            if os.path.exists(new_path):
                fixture_path = new_path
            else:
                full_path = os.path.split(full_path)[0]
            if current_level == max_levels:
                break
            current_level += 1
        if fixture_path is None:
            started_at = (environ.Path(__file__) - 1).root
            raise ValueError('Could not find fixtures folder in {}'.format(started_at))

        json_filename = '{}{}{}'.format(fixture_path, os.sep, filename)
        with open(json_filename, 'r', encoding='utf-8') as jfile:
            json_data = json.load(jfile)
        return json_data
