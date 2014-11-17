Name:           ros-hydro-applanix-bridge
Version:        0.0.5
Release:        0%{?dist}
Summary:        ROS applanix_bridge package

Group:          Development/Libraries
License:        BSD
URL:            http://wiki.ros.org/applanix_bridge
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-hydro-applanix-msgs
Requires:       ros-hydro-diagnostic-msgs
Requires:       ros-hydro-geodesy
Requires:       ros-hydro-geometry
Requires:       ros-hydro-message-runtime
Requires:       ros-hydro-rospy
BuildRequires:  pcapy
BuildRequires:  python-impacket
BuildRequires:  ros-hydro-applanix-msgs
BuildRequires:  ros-hydro-catkin
BuildRequires:  ros-hydro-rospy

%description
Contains the adapter node which translates between the Applanix serialized
socket format and ROS messages. This node is implemented in Python for now, but
could be re-implemented using roscpp if performance is a bottleneck.

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/hydro/setup.sh" ]; then . "/opt/ros/hydro/setup.sh"; fi
mkdir -p build && cd build
%cmake .. \
        -UINCLUDE_INSTALL_DIR \
        -ULIB_INSTALL_DIR \
        -USYSCONF_INSTALL_DIR \
        -USHARE_INSTALL_PREFIX \
        -ULIB_SUFFIX \
        -DCMAKE_INSTALL_PREFIX="/opt/ros/hydro" \
        -DCMAKE_PREFIX_PATH="/opt/ros/hydro" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/hydro/setup.sh" ]; then . "/opt/ros/hydro/setup.sh"; fi
cd build
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/hydro

%changelog
* Mon Nov 17 2014 Kareem Shehata <kshehata@clearpathrobotics.com> - 0.0.5-0
- Autogenerated by Bloom

