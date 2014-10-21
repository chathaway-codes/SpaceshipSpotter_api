from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from optparse import make_option
import h5py
import time
import os

from spaceship_spotter_api.models import *

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--filename',
            type="string",
            dest="filename",
            help="Where should we save the results?"
        ),
    )

    BASE_DIR = ''


    def handle(self, *args, **options):

        if options['filename'] == None:
            self.stdout.write("Please specify a filename with --filename")
            return

        self.filepath = os.path.join(self.BASE_DIR, options['filename'])
        self.stdout.write("Saving HDF5 to %s" % self.filepath)

        # Open the file for saving
        self.file = h5py.File(self.filepath)

        # We are going to store with the following format:
        # <report>/<reading> -- values
        # So we need to make a high-level list of readings, including the attributes
        # report - location, timestamp
        # reading - sensor, type, accuracy, timestamp
        # Then the readings contain a dataset of the values model

        for report in Report.objects.all():
            # Create report
            report_group = self.file.create_group("report-%s" % report.id)
            # Attach attributes
            report_group.attrs.create("location", (report.lat, report.lon))
            report_group.attrs.create("timestamp", str(report.timestamp))
            for reading in report.reading_set.all():
                # Create reading
                reading_ds = report_group.create_dataset("reading-%s" % reading.id, (reading.values_set.count(),))
                # Attach attributes
                reading_ds.attrs.create("sensor", str(reading.sensor))
                reading_ds.attrs.create("type", str(reading.type))
                reading_ds.attrs.create("accuracy", reading.accuracy)
                reading_ds.attrs.create("timestamp", str(reading.timestamp))
                # Record values
                for i, v in enumerate(reading.values_set.all()):
                    reading_ds[i] = v.value

        # Close the file
        self.file.close()
