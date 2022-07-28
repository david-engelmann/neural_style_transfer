# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.217.4/containers/ubuntu/.devcontainer/base.Dockerfile

# [Choice] Ubuntu version (use hirsute or bionic on local arm64/Apple Silicon): hirsute, focal, bionic
ARG VARIANT="dev-hirsute"
FROM mcr.microsoft.com/vscode/devcontainers/base:${VARIANT} as ubuntu_base
ENV VARIANT $VARIANT

FROM ubuntu_base as os_build

# Set based on Ubuntu Version - Hirsute = 21.04
ARG UBUNTU_VERSION="21.04"
ENV UBUNTU_VERSION $UBUNTU_VERSION

# [Choice] Python Version
ARG PYTHON_VERSION="3.9"
ENV PYTHON_VERSION $PYTHON_VERSION

# [Choice] Virtual Enviroment Path
ENV VIRTUAL_ENV="/opt/venv"
ARG VIRTUAL_ENV $VIRTUAL_ENV

# [Choice] Enviroment Type: "dev", "prod", "stage"
ARG ENV_TYPE="dev"
ENV ENV_TYPE $ENV_TYPE

# [Choice] Project Name: neural_style_transfer 
ARG PROJECT_NAME="neural_style_transfer"
ENV PROJECT_NAME $PROJECT_NAME

# [Choice] Project Version: 1, 1.0.0, latest
ARG PROJECT_VERSION=1
ENV PROJECT_VERSION $PROJECT_VERSION

# Add a Maintainer Label
LABEL maintainer="david-engelmann"

COPY ./.devcontainer/scripts/os_packages.sh . 
RUN sudo chmod +x ./os_packages.sh && bash ./os_packages.sh

## Section to install additional OS packages.
#RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#	&& apt-get -y install --no-install-recommends \
##		build-essential \
##		libpython3-dev \
##		python3 \
##		python3-pip \
##		python3-wheel \
#		#python${PYTHON_VERSION}-dev \
#		#python${PYTHON_VERSION}-venv \
##		software-properties-common \
##		python3-dev \
##		python3-venv \
##		python3-setuptools \
#        # Additional Vim Installs
#        vim \
#        fonts-powerline \
#	&& apt-get update && apt-get -y upgrade

COPY ./.devcontainer/scripts/vim_setup.sh . 
RUN sudo chmod +x ./vim_setup.sh && bash ./vim_setup.sh

# Change to Project Base Folder
WORKDIR /workspaces/neural_style_transfer

#ENTRYPOINT ["/python_packages.sh"]

# Make venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY requirements.txt .

COPY ./.devcontainer/scripts/python_packages.sh . 
RUN sudo chmod +x ./python_packages.sh && bash ./python_packages.sh

#RUN python3 -m venv /workspaces/neural_style_transfer/${VIRTUAL_ENV}
#ENV PATH="$VIRTUAL_ENV/bin:$PATH"
#RUN . ./$VIRTUAL_ENV/bin/activate

#COPY ./requirements.txt .

#RUN pip3 install --upgrade pip setuptools wheel \
	#&& pip3 install --no-cache-dir -r requirements.txt

FROM ubuntu_base as final

# Get local vimrc
COPY ./.devcontainer/local/vim /usr/share/vim

WORKDIR /workspaces/neural_style_transfer
COPY --from=os_build /bin /bin
COPY --from=os_build /etc /etc
COPY --from=os_build /sbin /sbin
COPY --from=os_build /lib /lib
#COPY --from=os_build /lib32 /lib32
#COPY --from=os_build /lib64 /lib64
COPY --from=os_build /opt /opt
COPY --from=os_build /proc /proc
COPY --from=os_build /sys /sys
COPY --from=os_build /usr /usr
COPY --from=os_build /var /var
COPY --from=os_build /dev /dev

# Get Virtual Env
ENV VIRTUAL_ENV="/opt/venv"
COPY --from=os_build ${VIRTUAL_ENV} ${VIRTUAL_ENV}

RUN alias python=python3

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./.devcontainer/scripts/venv_activation.sh . 
RUN sudo chmod +x ./venv_activation.sh && bash ./venv_activation.sh

COPY neural_style_transfer/neural_style_transfer.py .


#CMD ["/bin/bash"]
