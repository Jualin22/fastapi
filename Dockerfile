# use predefined python image
FROM python:3.9.7

# define working directory of container
WORKDIR /usr/src/app

# copy requirements file extra so package installation is only changed if this changes
COPY requirements.txt ./

# install packages from requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything
COPY . .

# command to start the app (all spaces are seperated through comma)
CMD ["uvicorn", "app.main.app", "--host", "0.0.0.0", "--port", "8000"]