Name:           ros-hydro-applanix-msgs
Version:        0.0.8
Release:        0%{?dist}
Summary:        ROS applanix_msgs package

Group:          Development/Libraries
License:        BSD
URL:            http://wiki.ros.org/applanix_msgs
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-hydro-geometry-msgs
Requires:       ros-hydro-message-runtime
Requires:       ros-hydro-rospy
BuildRequires:  ros-hydro-catkin
BuildRequires:  ros-hydro-geometry-msgs
BuildRequires:  ros-hydro-message-generation
BuildRequires:  ros-hydro-rospy

%description
ROS messages which represent the serialized wire messages and groups of Applanix
devices.

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/hydro/setup.sh" ]; then . "/opt/ros/hydro/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
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
cd obj-%{_target_platform}
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/hydro

%changelog
* Tue Mar 10 2015 Kareem Shehata <kshehata@clearpathrobotics.com> - 0.0.8-0
- Autogenerated by Bloom

* Sat Feb 28 2015 Kareem Shehata <kshehata@clearpathrobotics.com> - 0.0.7-0
- Autogenerated by Bloom

* Thu Dec 11 2014 Kareem Shehata <kshehata@clearpathrobotics.com> - 0.0.6-0
- Autogenerated by Bloom

* Mon Nov 17 2014 Kareem Shehata <kshehata@clearpathrobotics.com> - 0.0.5-0
- Autogenerated by Bloom

