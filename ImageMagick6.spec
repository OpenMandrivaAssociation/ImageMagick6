%define _disable_ld_no_undefined 1
# ImageMagick actually uses libtool to load its modules
%define dont_remove_libtool_files 1
%define build_test 0
%bcond_without bootstrap

# some other funny version
# (aw) from the docs: Versions with Q8 in the name are 8 bits-per-pixel
# component (e.g. 8-bit red, 8-bit green, etc.), whereas, Q16 in the
# filename are 16 bits-per-pixel component. A Q16 version permits you
# to read or write 16-bit images without losing precision but requires
# twice as much resources as the Q8 version.
%define qlev Q16

# their "official" version
%define rversion %(echo %{version} |cut -d. -f1-3)
# their "minor" version
%define minor_rev %(echo %{version} |cut -d. -f4)
# the full file version
%define dversion %{rversion}-%{minor_rev}

%define api	6
%define major	7
%define cppmajor 9
%define libMagickpp %mklibname Magick++ %{api}.%{qlev} %{cppmajor}
%define libMagickCore %mklibname MagickCore %{api}.%{qlev} %{major}
%define libMagickWand %mklibname MagickWand %{api}.%{qlev} %{major}
%define devname %mklibname magick -d

Summary:	An X application for displaying and manipulating images
Name:		imagemagick6
Version:	6.9.13.54
Release:	2
License:	BSD-like
Group:		Graphics
Url:		https://legacy.imagemagick.org/
Source0:	https://imagemagick.org/archive/releases/ImageMagick-%{dversion}.tar.xz
# Also:	https://github.com/ImageMagick/ImageMagick6/archive/%{dversion}/ImageMagick-%{dversion}.tar.gz
Source1:	ImageMagick.pdf.bz2
Source2:	%{name}.rpmlintrc
# re-scaled from ftp://ftp.imagemagick.org/pub/ImageMagick/images/magick-icon.png
Source10:	magick-icon_16x16.png
Source11:	magick-icon_32x32.png
Source12:	magick-icon_48x48.png
Source13:	magick-icon_64x64.png
Patch0:		perlmagick.rpath.patch
Patch2:		imagemagick6-6.9.9-openmp-linkage.patch
Patch7:		imagemagick-urw.diff
Patch17:	imagemagick-fpx.diff
Patch19:	ImageMagick-libpath.diff
#Patch20:	imagemagick-6.8.3-pkgconfig.patch
# OpenCL already uses libc dlopen; close with dlclose (not lt_dlclose) and
# prefer the runtime soname (libOpenCL.so is only in -devel).
Patch21:	imagemagick6-opencl-dlopen.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool-base
BuildRequires:	slibtool
BuildRequires:	pkgconfig(sltdl)
BuildRequires:	make
BuildRequires:	chrpath
BuildRequires:	ghostscript
BuildRequires:	subversion
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	jbig-devel
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	libtool-devel
BuildRequires:	libwmf-devel
BuildRequires:	perl-devel
BuildRequires:	libatomic-devel
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(jasper)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(libjxl)
BuildRequires:	pkgconfig(libgvc)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(lqr-1)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(OpenCL)
%if ! %{with bootstrap}
BuildRequires:	pkgconfig(ddjvuapi)
%endif

%description
ImageMagick is a powerful image display, conversion and manipulation tool. It
runs in an X session. With this tool, you can view, edit and display a variety
of image formats.

ImageMagick can make use of the following delegate programs, available as
packages in Mandriva Linux: curl enscript ffmpeg ghostscript ghostscript-X gimp
gnuplot graphviz html2ps mplayer ncompress netpbm sane-backends tetex-dvips
transfig ufraw xdg-utils zip autotrace povray

%package 	desktop
Summary:	ImageMagick menus
Group:		Graphics
Requires:	xterm

%description	desktop
This package contains the menu and .desktop entries to run the "display"
command from the menu.

%package -n	%{libMagickpp}
Summary:	ImageMagick libraries
Group:		System/Libraries
Obsoletes:	%{_lib}magick6 < 6.8.5.6-1

%description -n	%{libMagickpp}
This package contains a library for %{name}.

%package -n	%{libMagickCore}
Summary:	ImageMagick libraries
Group:		System/Libraries
Conflicts:	%{_lib}magick6 < 6.8.5.6-1

%description -n	%{libMagickCore}
This package contains a library for %{name}.

%package -n	%{libMagickWand}
Summary:	ImageMagick libraries
Group:		System/Libraries
Conflicts:	%{_lib}magick6 < 6.8.5.6-1

%description -n	%{libMagickWand}
This package contains a library for %{name}.

%package -n	%{devname}
Summary:	Development libraries and header files for ImageMagick app development
Group:		Development/C
Requires:	%{libMagickpp} = %{version}-%{release}
Requires:	%{libMagickCore} = %{version}-%{release}
Requires:	%{libMagickWand} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
If you want to create applications that will use ImageMagick code or APIs,
you'll need to install these packages as well as ImageMagick. These additional
packages aren't necessary if you simply want to use ImageMagick, however.

ImageMagick-devel is an addition to ImageMagick which includes development
libraries and header files necessary to develop applications.

%package -n	perl-Image-Magick
Summary:	Libraries and modules for access to ImageMagick from perl
Group:		Development/Perl
Requires:	%{name} = %{version}
Requires:	graphviz
Requires:	libwmf

%description -n	perl-Image-Magick
This is the ImageMagick perl support package. It includes perl modules and
support files for access to ImageMagick library from perl.

%package	doc
Summary:	%{name} Documentation
Group:		Books/Other
BuildArch:	noarch

%description	doc
This package contains HTML/PDF documentation of %{name}.

%prep
%autosetup -p1 -n ImageMagick-%{rversion}-%{minor_rev}

bzcat %{SOURCE1} > ImageMagick.pdf
install -m 644 %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} .
libtoolize --copy --force; aclocal -I m4; autoconf; automake -a

%build
#gw the format-string patch is incomplete:
%define Werror_cflags %nil
# Keep ${CFLAGS}/${CXXFLAGS} so a %%pgo pass can inject -fprofile-generate/use
export CFLAGS="${CFLAGS:-%{optflags}} -fno-strict-aliasing -fPIC"
export CXXFLAGS="${CXXFLAGS:-%{optflags}} -fno-strict-aliasing -fPIC"

%configure \
	--disable-static \
	--docdir=%{_defaultdocdir}/imagemagick \
	--with-pic \
	--enable-shared \
	--enable-fast-install \
	--disable-ltdl-install \
	--with-threads \
	--with-magick_plus_plus \
	--with-gslib \
	--with-wmf \
	--without-lcms \
	--with-lcms2 \
	--with-xml \
	--without-dps \
	--without-windows-font-dir \
	--with-modules \
	--with-perl \
	--with-perl-options="INSTALLDIRS=vendor CCFLAGS='${CFLAGS}' CC='%{__cc} -L$PWD/magick/.libs' LDDLFLAGS='${LDFLAGS:-%{?build_ldflags}} -shared -L$PWD/magick/.libs'" \
	--with-jp2 \
	--with-jxl \
	--with-gvc \
	--with-lqr \
	--enable-opencl

# Disable rpath
#sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
#sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# Fix syntax errors
find PerlMagick -name "*.PL" |xargs sed -i -e "s,'\$,';,g"

%make_build

# Train the instrumented convert/identify and MagickWand/Magick++ on the
# paths that dominate real use. Optional delegates are skipped if missing.
# No X11.
# slibtool writes coder .so files to .libs/ but the .la dlname is just
# "foo.so", so lt_dlopen looks next to the .la (not in .libs/).
%pgo
set +e
export LLVM_PROFILE_FILE="%{_pgo_profile_dir}/imagemagick6-%%m-%%p.profraw"
# Do not let a GPU on the build host own the profile. CPU OpenCL (pocl
# etc.) still trains the host enqueue path; if no CPU ICD exists, IM
# falls back to the OpenMP implementations and those stay hot.
export MAGICK_OCL_DEVICE=CPU

TOP="$PWD"
tool() {
	t="$TOP/utilities/.libs/$1"
	[ -x "$t" ] || t="$TOP/utilities/$1"
	echo "$t"
}
CONVERT=$(tool convert)
IDENTIFY=$(tool identify)
COMPARE=$(tool compare)
MONTAGE=$(tool montage)
MOGRIFY=$(tool mogrify)
STREAM=$(tool stream)
COMPOSITE=$(tool composite)
if [ ! -x "$CONVERT" ]; then
	echo "PGO: instrumented convert missing"
	exit 1
fi
for d in "$TOP/coders" "$TOP/filters"; do
	if [ -d "$d/.libs" ]; then
		( cd "$d" && for so in .libs/*.so; do
			[ -e "$so" ] || continue
			ln -sfn "$so" "$(basename "$so")"
		done )
	fi
done
export LD_LIBRARY_PATH="$TOP/magick/.libs:$TOP/wand/.libs:$TOP/Magick++/lib/.libs${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export MAGICK_CODER_MODULE_PATH="$TOP/coders"
export MAGICK_FILTER_MODULE_PATH="$TOP/filters"
export MAGICK_CONFIGURE_PATH="$TOP/config"

im() {
	"$CONVERT" "$@"
}
try() {
	im "$@"
	rc=$?
	if [ $rc -ne 0 ]; then
		echo "PGO: skipped (exit $rc): convert $*"
	fi
	return 0
}

WORKDIR="$PWD/pgo-train"
rm -rf "$WORKDIR"
mkdir -p "$WORKDIR"
cd "$WORKDIR"

im logo: logo.png || exit 1
im wizard: wizard.png || exit 1
im rose: rose.png || exit 1
try granite: granite.png
try netscape: netscape.gif
try -size 1280x720 plasma:fractal photo.png
if [ ! -f photo.png ]; then
	im logo: -resize 1280x720 photo.png || exit 1
fi
try -size 640x360 gradient:black-white gradient.png
try -size 320x240 xc:'#224466' solid.png
try -size 400x80 -background white -fill black -pointsize 28 caption:'ImageMagick PGO' caption.png

for fmt in jpg png webp gif tiff bmp ppm pam miff; do
	try photo.png -quality 85 "enc.$fmt"
	try "enc.$fmt" "round.png"
done
try rose.png enc.ico
try enc.ico ico-round.png
try photo.png -quality 82 -sampling-factor 4:2:0 jpeg420.jpg
try photo.png -interlace Plane -quality 80 jpegprog.jpg
try photo.png -colorspace Gray -quality 80 jpeggray.jpg
try wizard: -resize 400x PNG32:alpha.png
try alpha.png -background none -resize 200x alpha-small.png
try -delay 8 -loop 0 logo: -resize 120x \
	\( +clone -roll +8+0 \) \( +clone -roll +0+8 \) anim.gif
try anim.gif -coalesce -resize 80x -layers optimize anim-opt.gif

try photo.png out.jxl
try photo.png out.jp2
try rose.png out.svg
try photo.png pdf:out.pdf
try 'out.pdf[0]' pdfpage.png
if [ -f ../tests/rose.pnm ]; then
	try ../tests/rose.pnm rose-pnm.png
fi

try photo.png -auto-orient -resize '1024x1024>' -strip -quality 82 web.jpg
try photo.png -thumbnail 150x150^ -gravity center -extent 150x150 thumb.jpg
try photo.png -crop 640x360+80+40 +repage crop.png
try photo.png -rotate 90 rot.png
try photo.png -flip -flop flip.png
try photo.png -resize 50% -unsharp 0x0.75+0.75+0.008 unsharp.jpg
try photo.png -gaussian-blur 0x1.2 blur.png
try photo.png -sharpen 0x1.0 sharp.png
try photo.png -modulate 105,110,100 mod.png
try photo.png -level 5%,95% level.png
try photo.png -normalize norm.png
try photo.png -colorspace sRGB srgb.png
try photo.png -colorspace Gray gray.png
try photo.png -colorspace CMYK cmyk.jpg
try photo.png -gamma 1.1 gamma.png
try photo.png -posterize 16 post.png
try photo.png -colors 64 +dither pal.png
try photo.png -trim +repage trim.png
try photo.png -bordercolor white -border 8 border.png
try photo.png -resize 800x -quality 70 -strip -interlace Plane web-sm.jpg
try rose.png -liquid-rescale 50%x50% lqr.png

try photo.png -gravity southeast -pointsize 22 -fill white \
	-annotate +16+16 'PGO watermark' annotated.jpg
try photo.png caption.png -gravity south -geometry +0+10 -compose over -composite marked.png
try -size 200x200 xc:none -fill '#cc3333' -draw 'circle 100,100 100,20' ball.png
try photo.png ball.png -gravity northeast -geometry +20+20 -compose over -composite badged.png

if [ -x "$IDENTIFY" ]; then
	"$IDENTIFY" -verbose photo.png
	"$IDENTIFY" jpeg420.jpg enc.png anim.gif
fi
if [ -x "$COMPARE" ]; then
	"$COMPARE" -metric RMSE photo.png web.jpg diff.png
fi
if [ -x "$MONTAGE" ]; then
	"$MONTAGE" logo.png wizard.png rose.png -geometry 120x120+4+4 -tile 3x1 sheet.png
fi
if [ -x "$MOGRIFY" ]; then
	"$MOGRIFY" -resize 320x -quality 80 jpeg420.jpg
fi
if [ -x "$STREAM" ]; then
	"$STREAM" -map rgb -storage-type char rose.png stream.rgb
fi

cd "$TOP"
make %{?_smp_mflags} tests/wandtest tests/validate \
	Magick++/tests/appendImages Magick++/tests/readWriteImages \
	Magick++/tests/attributes Magick++/tests/color \
	Magick++/tests/montageImages Magick++/tests/morphImages \
	Magick++/tests/averageImages Magick++/tests/coalesceImages
[ -x tests/wandtest ] && tests/wandtest
if [ -x tests/validate ]; then
	for kind in convert identify compare composite montage stream colorspace; do
		tests/validate -validate "$kind"
	done
fi
export SRCDIR="$TOP/Magick++/tests/"
for t in appendImages readWriteImages attributes color montageImages \
	morphImages averageImages coalesceImages; do
	if [ -x Magick++/tests/$t ]; then
		Magick++/tests/$t
	fi
done

rm -rf "$WORKDIR"
exit 0

%if %{build_test}
%check
# these tests require X
if [ -f PerlMagick/t/x11/read.t ]; then
	mv PerlMagick/t/x11/read.t PerlMagick/t/x11/read.t.disabled
fi
if [ -f PerlMagick/t/x11/write.t ]; then
	mv PerlMagick/t/x11/write.t PerlMagick/t/x11/write.t.disabled
fi
#dlname=`grep "^dlname" Magick++/lib/.libs/libMagick++.la | cut -d\' -f2`
#LD_PRELOAD="$PWD/Magick++/lib/.libs/$dlname" VERBOSE="1" make check
make check
%endif

%install
# (Abel) set LD_RUN_PATH to null, to avoid adding rpath to perlmagick module
%makeinstall_std LD_RUN_PATH="" pkgdocdir=/installed_docs

# fix docs inclusion (fix an unknown new rpm bug)
rm -rf installed_docs; mv %{buildroot}/installed_docs .

# Remove unpackaged files
find %{buildroot} -name '*.la' -type f -delete
rm -f %{buildroot}%{_libdir}/libltdl* 

# create compatible symlinks
ln -s libMagick++-%{api}.%{qlev}.so %{buildroot}%{_libdir}/libMagick++.so
ln -s libMagickCore-%{api}.%{qlev}.so %{buildroot}%{_libdir}/libMagickCore.so
ln -s libMagickWand-%{api}.%{qlev}.so %{buildroot}%{_libdir}/libMagickWand.so

# icons
install -m 755 -d %{buildroot}%{_liconsdir} \
	   %{buildroot}%{_iconsdir} \
	   %{buildroot}%{_iconsdir}/hicolor/64x64/apps \
           %{buildroot}%{_miconsdir}
install -m 644 magick-icon_16x16.png %{buildroot}%{_miconsdir}/%{name}.png
install -m 644 magick-icon_32x32.png %{buildroot}%{_iconsdir}/%{name}.png
install -m 644 magick-icon_48x48.png %{buildroot}%{_liconsdir}/%{name}.png
install -m 644 magick-icon_64x64.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png

install -m 755 -d %{buildroot}%{_datadir}/applications/
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=ImageMagick
Name[ru]=ImageMagick
Comment=Views Graphics files
Comment[ru]=Просмотр графических файлов
Exec=%{_bindir}/xterm -geometry 40x15 -title ImageMagick +sb -iconic -e %{_bindir}/display
Icon=%{name}
Terminal=false
Type=Application
Categories=Graphics;Viewer;
EOF

%files
%doc README.txt
%doc %{_docdir}/ImageMagick-6
%{_sysconfdir}/ImageMagick-6
%{_bindir}/animate
%{_bindir}/compare
%{_bindir}/composite
%{_bindir}/convert
%{_bindir}/conjure
%{_bindir}/display
%{_bindir}/identify
%{_bindir}/import
%{_bindir}/mogrify
%{_bindir}/montage
%{_bindir}/stream
%dir %{_libdir}/ImageMagick-%{rversion}
%dir %{_libdir}/ImageMagick-%{rversion}/modules-%{qlev}
%dir %{_libdir}/ImageMagick-%{rversion}/modules-%{qlev}/coders
%{_libdir}/ImageMagick-%{rversion}/modules-%{qlev}/coders/*
%dir %{_libdir}/ImageMagick-%{rversion}/modules-%{qlev}/filters
%{_libdir}/ImageMagick-%{rversion}/modules-%{qlev}/filters/*
%{_libdir}/ImageMagick-%{rversion}/config-%{qlev}
%{_datadir}/ImageMagick-6
%doc %{_mandir}/man1/*
%doc %{_mandir}/man3/*
%exclude %{_mandir}/man3/*::*.3pm*

%files desktop
%{_datadir}/applications/*
%{_iconsdir}/%{name}.png
%{_iconsdir}/hicolor/64x64/apps/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png

%files -n %{libMagickpp}
%{_libdir}/libMagick++-%{api}.%{qlev}.so.%{cppmajor}*

%files -n %{libMagickCore}
%{_libdir}/libMagickCore-%{api}.%{qlev}.so.%{major}*

%files -n %{libMagickWand}
%{_libdir}/libMagickWand-%{api}.%{qlev}.so.%{major}*

%files -n %{devname}
%{_includedir}/ImageMagick-%{api}
%{_bindir}/Magick-config
%{_bindir}/Magick++-config
%{_bindir}/MagickCore-config
%{_bindir}/MagickWand-config
%{_bindir}/Wand-config
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files -n perl-Image-Magick
%{perl_vendorarch}/Image
%{perl_vendorarch}/auto/Image
%doc %{_mandir}/man3*/*::*.3pm*

%files doc
%doc ImageMagick.pdf LICENSE NEWS* NOTICE
%doc QuickStart.txt installed_docs/*
