from mamba import description, it, before, context
from expects import expect, have_key, be_none

import securecscc
from securecscc import origins

from specs.support import fixtures
from specs.support.matchers import be_an_uuid


with description(origins.Falco) as self:
    with before.each:
        self.settings = securecscc.Settings()
        self.mapper = origins.Falco(self.settings)

    with it('uses the source_id assigned to us from Google'):
        finding = self.mapper.create_from(fixtures.event_falco())

        expect(finding).to(have_key('source_id', self.settings.source_id()))

    with it('uses the rule as category'):
        category = 'Terminal shell in container'

        finding = self.mapper.create_from(fixtures.event_falco())

        expect(finding).to(have_key('category', category))

    with it('uses only seconds from event time'):
        event_time = 1526547969

        finding = self.mapper.create_from(fixtures.event_falco())

        expect(finding).to(have_key('event_time', event_time))

    with it('does not set any url'):
        finding = self.mapper.create_from(fixtures.event_falco())

        expect(finding).to(have_key('url', be_none))

    with it('uses an uuid as id'):
        finding = self.mapper.create_from(fixtures.event_falco())

        expect(finding).to(have_key('id', be_an_uuid()))

    with it('uses organization as asset ids'):
        finding = self.mapper.create_from(fixtures.event_falco())

        expect(finding).to(have_key('asset_ids', [self.settings.organization()]))

    with context('when building properties'):
        with it('adds output'):
            output = "A shell was spawned in a container with an attached terminal (user=root unruffled_hamilton (id=32c415f00958) shell=bash parent=<NA> cmdline=bash  terminal=34816)"

            finding = self.mapper.create_from(fixtures.event_falco())

            expect(finding).to(have_key('properties', have_key('summary', output)))

        with it('adds priority'):
            finding = self.mapper.create_from(fixtures.event_falco())

            expect(finding).to(have_key('properties', have_key('priority', 'Notice')))

        with it('adds container id'):
            finding = self.mapper.create_from(fixtures.event_falco())

            expect(finding).to(have_key('properties', have_key('container.id', '32c415f00958')))

        with it('adds container name'):
            finding = self.mapper.create_from(fixtures.event_falco())

            expect(finding).to(have_key('properties', have_key('container.name', 'unruffled_hamilton')))

    with context('when creating from falco with kubernetes integration enabled'):
        with it('adds pod name to properties'):
            finding = self.mapper.create_from(fixtures.event_falco_k8s())

            expect(finding).to(have_key('properties', have_key('kubernetes.pod.name', 'falco-event-generator-6fd89678f9-cdkvz')))
