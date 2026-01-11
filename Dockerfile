FROM python:3.10

RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /home/user/app

COPY --chown=user . .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["python3", "-m", "AutoAnimeBot"]
