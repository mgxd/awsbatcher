# - download abide (datalad)
# - process (fmriprep)

FROM poldracklab/fmriprep:1.1.2

# install datalad + aws reqs
RUN apt-get update && \
    apt-get install -y --no-install-recommends groff \
                                               less \
                                               unzip \
                                               git-annex-standalone
# aws cli
RUN pip install --no-cache-dir awscli

# add AWS handshake script to container
COPY scripts/batch_runner.sh /
RUN chmod +x /batch_runner.sh


ENTRYPOINT ["/batch_runner.sh"]
