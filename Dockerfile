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

# license file
RUN echo "cHJpbnRmICJtYXRoaWFzZ0BtaXQuZWR1XG4yNzI1N1xuICpDWG5wZVB3Y2ZLYllcbkZTY3pvTFJBZG9pOHMiID4gL3RtcC8uZnNfbGljZW5zZS50eHQK" | base64 -d | sh

ENTRYPOINT ["/batch_runner.sh"]
