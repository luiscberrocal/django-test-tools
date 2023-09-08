from django.core.checks import register, Error, Tags


@register(Tags.compatibility, deploy=True)
def example_check(app_configs, **kwargs):
    errors = []
    check_failed = True

    if check_failed:
        errors.append(
            Error(
                'an error',
                hint='A hint.',
                obj='kKKK',
                id='myapp.E001',
            )
        )
    return errors
