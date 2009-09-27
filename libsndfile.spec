%define	major 1
%define	libname	%mklibname sndfile %{major}
%define develname %mklibname sndfile -d
%define staticname %mklibname sndfile -d -s
%define build_octave 0

%define bootstrap 0
%{?_without_bootstrap: %global bootstrap 0}
%{?_with_bootstrap: %global bootstrap 1}

Summary:	A library to handle various audio file formats
Name:		libsndfile
Version:	1.0.20
Release:	%mkrel 3
License:	LGPLv2+
Group:		Sound
URL:		http://www.mega-nerd.com/libsndfile/
Source0:	http://www.mega-nerd.com/libsndfile/%{name}-%{version}.tar.gz
BuildRequires:	libogg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	sqlite3-devel
BuildRequires:	libflac-devel
BuildRequires:	libalsa-devel
%if !%bootstrap
%ifarch %{ix86} x86_64
BuildRequires:	nasm
%endif
BuildRequires:	libjack-devel
BuildRequires:	libsamplerate-devel
%endif
BuildRequires:	celt-devel
BuildRequires:	autogen
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
libsndfile is a C library for reading and writing sound files such as
AIFF, AU and WAV files through one standard interface. It can currently
read/write 8, 16, 24 and 32-bit PCM files as well as 32-bit floating
point WAV files and a number of compressed formats.

%package -n %{libname}
Summary:	Shared library of sndfile
Group:		System/Libraries

%description -n	%{libname}
libsndfile is a C library for reading and writing sound files such as
AIFF, AU and WAV files through one standard interface. It can currently
read/write 8, 16, 24 and 32-bit PCM files as well as 32-bit floating
point WAV files and a number of compressed formats.

This package contains the shared library to run applications based on
libsndfile.

%package -n %{develname}
Summary:	Libraries, includes, etc to develop libsndfile applications 
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	libflac-devel
Provides:	sndfile-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname sndfile 1 -d

%description -n	%{develname}
Libraries, include files, etc you can use to develop libsndfile applications.

%package -n %{staticname}
Summary:	Static Library for developing libsndfile applications
Group:		Development/C
Requires:	%{develname} = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}
Obsoletes:	%mklibname sndfile 1 -d -s

%description -n	%{staticname}
This contains the static library of libsndfile needed for building apps that
link statically to libsndfile.

%package progs
Summary:	Example progs based on libsndfile
Group:		Sound 

%description	progs
This contains sndfile-info for printing information about a sound
file and sndfile-play for playing a sound file.


%if %build_octave
%package octave
Summary:	Octave modules based on libsndfile
Group:		Sound 
Conflicts: libsndfile-progs < 1.0.18-0.pre17.1mdv
BuildRequires:	octave3-devel

%description octave
This contains octave modules based on libsndfile for reading, writing and 
playing audio files.
%endif

%prep
%setup -qn %{name}-%{version}

%build
%configure2_5x
%make

%install
rm -rf %{buildroot} 

%makeinstall_std 
rm -rf %{buildroot}%{_includedir}/FLAC

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS NEWS README
%{_libdir}/libsndfile.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc %{_docdir}/libsndfile1-dev
%doc ChangeLog 
%attr(644,root,root) %{_libdir}/libsndfile.la
%{_libdir}/libsndfile.so
%{_includedir}/sndfile.h
%{_includedir}/sndfile.hh
%{_libdir}/pkgconfig/sndfile.pc

%files -n %{staticname}
%defattr(-,root,root)
%{_libdir}/libsndfile.a

%files progs
%defattr(-,root,root)
%{_bindir}/sndfile-*
%{_mandir}/man1/*

%if %build_octave
%files octave
%defattr(-,root,root)
%{_datadir}/octave/
%_libdir/octave/*/site/oct/*/*.oct
%endif
