from rest_framework import serializers
from django.utils.translation import ugettext as _
from configsetting.models import GlobalPreference
from mewtwo.lib import constants


class GlobalPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalPreference
        fields = ['key', 'value', 'display_name', 'type', 'note']

    def validate(self, data):
        key = self.context['view'].kwargs.get('key')

        # if need validation, should add method named 'validate_{key}'
        validate_function = \
            getattr(self, f'validate_{key}', self.default_validate)

        return validate_function(data)

    def default_validate(self, data):
        if self.context['request'].method == 'PATCH' and 'key' in data:
            raise serializers.ValidationError({
                constants.NOT_ALLOWED: _("Can't revise key")
            })

        if 'value' in data:
            # validate empty str
            data['value'] = data['value'].strip()
            key = self.context['view'].kwargs.get('key')

            # strip comma separated segments and store them for later usage
            # strip blanks for each comma separated sub_value
            segments = []
            for segment in data['value'].split(','):
                segments.append(segment.strip())
            data['sub_values'] = segments
            if len(data['sub_values']) > 1:
                data['value'] = ','.join(segments)

        return data

    def validate_throttle_rate(self, data):
        rate = data.get('value')
        num, period = rate.split('/')
        try:
            num_requests = int(num)
            if period[0] not in ['s', 'm', 'h', 'd']:
                raise serializers.ValidationError({
                        constants.FIELD_ERROR: _('Invalid rate value')
                    })
        except:
            raise serializers.ValidationError({
                        constants.FIELD_ERROR: _('Invalid rate value')
                    })
        return data
