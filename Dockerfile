FROM remotepixel/amazonlinux:gdal2.4-py3.7-cogeo

WORKDIR /tmp

ENV PYTHONUSERBASE=/var/task

COPY setup.py setup.py
COPY awspds_mosaic/ awspds_mosaic/

RUN pip install . --user
RUN pip install git+https://github.com/cogeotiff/rio-tiler.git@0ae299ab448921c0b4346af21bf1b5edf8d9eb46 --user
RUN rm -rf awspds_mosaic setup.py