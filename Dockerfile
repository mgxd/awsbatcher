# - download abide (datalad)
# - process (fmriprep)

FROM poldracklab/fmriprep:1.1.2

# install datalad + rclone reqs
RUN apt-get update && \
    apt-get install -y --no-install-recommends groff \
                                               less \
                                               unzip \
                                               git-annex-standalone

# install rclone
WORKDIR /tmp
RUN curl -o rclone.zip https://downloads.rclone.org/rclone-current-linux-amd64.zip && \
    unzip rclone.zip -d rclone && \
    mv rclone/*/rclone /usr/bin/rclone && \
    rm -rf /tmp/rclone*

RUN curl -fsSL -o rclone.conf https://www.dropbox.com/s/b2rch9upmp0t7oe/rclone_config.txt?dl=1 && \
    mv rclone.conf /root/.rclone.conf

RUN pip install --no-cache-dir awscli

# overwrite fmriprep entrypoint
# /usr/local/miniconda/bin/fmriprep
ENTRYPOINT []
