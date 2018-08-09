# - download abide (datalad)
# - process (fmriprep)

FROM poldracklab/fmriprep:1.1.4

# install datalad + aws reqs
RUN apt-get update && \
    apt-get install -y --no-install-recommends groff \
                                               less \
                                               netbase \
                                               unzip \
                                               git-annex-standalone
# aws cli
RUN pip install --no-cache-dir -U awscli pip

# add AWS handshake script to container
COPY scripts/batch_runner.sh /
RUN chmod +x /batch_runner.sh


ENTRYPOINT ["/batch_runner.sh"]
