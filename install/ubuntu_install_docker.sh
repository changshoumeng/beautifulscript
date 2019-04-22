#!/bin/bash
#title          :install.sh 
#usage          :sh install.sh
#notes          :Only for Ubuntu and Mint
#==============================================================================

# CONSTANTS
declare -r HOME=$(readlink -f ~)
  

# Questions
declare -i INSTALL_DOCKER=0
 
 

# PACKAGE VERSION
CURRENT_VERSION="0.1.0"
PACKAGE_VERSION="0.1.0"

# PARAMS
LOCAL_PACKAGE=""
UI_PACKAGE=""
declare -i DEPS_ONLY=0
declare -i DEVELOP=0

# @brief print error message
# @param error message
function error_msg()
{
    echo -e "\n\n\e[91m$@\e[39m\n" >&2
}

# @brief print warning message
# @param warning message
function warning_msg()
{
    echo -e "\n\n\e[93m$@\e[39m\n"
}

# @brief print info message
# @param info message
function info_msg()
{
    echo -e "\n\n\e[92m$@\e[39m\n"
}


# @brief ask user
# @param question
# @return 1 if answer is 'yes', 0 if 'no'
function ask_user()
{
    # if want to install only deps,
    # we don't have to ask if want to install any dependency
    [[ ${DEPS_ONLY} -eq 1 ]] && return 1
    while [ 1 ]; do
        read -p "$@ " yn
        case ${yn} in
            y|Y ) return 1;;
            n|N ) return 0;;
            * ) warning_msg "Please answer yes or no.";;
        esac
    done
}

 

# @brief check if dependencies (Docker, nvidia-docker + nvidia-modprobe)
# are installed and set proper 'global' variables
function check_dependencies()
{
    # Check if docker daemon exists
    if [[ -z "$( service --status-all 2>&1 | grep -F 'docker' )" ]]; then
        ask_user "Docker not found. Do you want to install it? (y/n)"
        INSTALL_DOCKER=$?
    else
        info_msg "Docker is already installed"
    fi 
 
}


# @brief Install/Upgrade required dependencies
function install_dependencies()
{
    info_msg "INSTALLING GOLEM DEPENDENCIES"
    sudo id &> /dev/null
    if [[ $? -ne 0 ]]; then
        error_msg "Dependency installation requires sudo privileges"
        exit 1
    fi

    declare -a packages=( openssl pkg-config \
               libssl-dev autoconf  )

    if [[ ${INSTALL_DOCKER} -eq 1 ]]; then
        info_msg "INSTALLING DOCKER"

        # Ubuntu 14.04 needs some additional dependencies
        if [[ $( lsb_release -r | awk '{print $2}' ) == '14.04' ]]; then
            packages+=("linux-image-extra-$(uname -r)" linux-image-extra-virtual)
        fi

        packages+=( apt-transport-https \
                    ca-certificates \
                    software-properties-common)
        wget -qO- https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
        sudo add-apt-repository \
            "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
            $(lsb_release -cs) \
            stable"
    fi

    docker_version="$(apt-cache madison docker-ce 2>/dev/null | head -1 | awk '{print $3}')"
    if [[ -z "${docker_version}" ]]; then
        packages+=(docker-ce)
    else
        packages+=(docker-ce=${docker_version})
    fi
	
    sudo apt-get update >/dev/null
    echo -e "\e[91m"
    for package in ${packages[*]}; do
        sudo apt-get install -q -y ${package} >/dev/null
    done
    echo -e "\e[39m"
    if [[ ${INSTALL_DOCKER} -eq 1 ]]; then
        if [[ -z "${SUDO_USER}" ]]; then
            sudo usermod -aG docker ${USER}
        else
            sudo usermod -aG docker ${SUDO_USER}
        fi
        sudo docker run hello-world &>/dev/null
        if [[ ${?} -eq 0 ]]; then
            info_msg "Docker installed successfully"
        else
            warning_msg "Error occurred during installation"
            sleep 5s
        fi
    fi

    info_msg "Done installing Golem dependencies"
}

 

 


# @brief Main function
function main()
{
    check_dependencies
    install_dependencies
    [[ ${DEPS_ONLY} -eq 1 ]] && return 
    result=$?
    if [[ ${INSTALL_DOCKER} -eq 1 ]]; then
        info_msg "You need to restart your PC to finish installation"
    fi
    if [[ ${result} -ne 0 ]]; then
        error_msg "Installation failed"
    fi
    return ${result}
}
  

main
exit $?