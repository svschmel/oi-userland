#
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# You can obtain a copy of the license at usr/src/OPENSOLARIS.LICENSE
# or http://www.opensolaris.org/os/licensing.
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at usr/src/OPENSOLARIS.LICENSE.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
#

#
# Copyright (c) 2011, 2017, Oracle and/or its affiliates. All rights reserved.
# Copyright (c) 2019, Michal Nowak
#

PREFERRED_BITS=	64

include ../../../make-rules/shared-macros.mk

COMPONENT_NAME=		Python
COMPONENT_VERSION=	3.5.7
COMPONENT_PROJECT_URL=	https://www.python.org
COMPONENT_SRC=		$(COMPONENT_NAME)-$(COMPONENT_VERSION)
COMPONENT_ARCHIVE=	$(COMPONENT_SRC).tar.xz
COMPONENT_ARCHIVE_HASH=	\
	sha256:285892899bf4d5737fd08482aa6171c6b2564a45b9102dfacfb72826aebdc7dc
COMPONENT_ARCHIVE_URL=	$(COMPONENT_PROJECT_URL)/ftp/python/$(COMPONENT_VERSION)/$(COMPONENT_ARCHIVE)
COMPONENT_SIG_URL=	$(COMPONENT_ARCHIVE_URL).asc

CONFIGURE_FIX_LIBTOOL_RPATH = no

include $(WS_MAKE_RULES)/prep.mk
include $(WS_MAKE_RULES)/configure.mk
include $(WS_MAKE_RULES)/ips.mk

# Need to preserve timestamp for Grammar files.  If the pickle files are older,
# Python will try to rebuild them.
PKGSEND_PUBLISH_OPTIONS += -T \*Grammar\*.txt
PKGSEND_PUBLISH_OPTIONS += -T \*Grammar\*.pickle

# We patch auto* files, so regenerate headers and configure
COMPONENT_PREP_ACTION = \
	( cd $(@D) ; autoheader ; autoconf -f )

# The DTrace patch needs this file to be mode 0755.
COMPONENT_PRE_BUILD_ACTION=($(CHMOD) +x \
    $(SOURCE_DIR)/Include/pydtrace_offsets.sh)

# we don't want to leak $(CC_BITS) into BASECFLAGS as it causes problems with
# python-config
CC +=	$(CFLAGS)

C99MODE=
CPPFLAGS +=	-IPython

# to find the ncurses headers
CPPFLAGS +=	-I/usr/include/ncurses
# enable large files how they did in JDS
CPPFLAGS +=	-D_LARGEFILE64_SOURCE

# libffi for _ctypes
CPPFLAGS +=	$(shell pkg-config --cflags-only-I libffi)

# because python links with $(CC) ... $(LDFLAGS) ...
LDFLAGS =	$(CC_BITS) $(CC_PIC)

# build pic
CFLAGS +=	$(CC_PIC)

# XPG6
CFLAGS +=	-std=c99 -D_XOPEN_SOURCE=600

# add /usr/gnu/lib to the library search/run path
LDFLAGS.64 = -R/usr/gnu/lib/$(MACH64) -L/usr/gnu/lib/$(MACH64)
LDFLAGS += $(LDFLAGS.$(BITS))

CONFIGURE_OPTIONS  +=		--infodir=$(CONFIGURE_INFODIR)
CONFIGURE_OPTIONS  +=		--enable-shared
CONFIGURE_OPTIONS  +=		--with-dtrace
CONFIGURE_OPTIONS  +=		--with-system-expat
CONFIGURE_OPTIONS  +=		--with-system-ffi
CONFIGURE_OPTIONS  +=		--without-gcc
CONFIGURE_OPTIONS  +=		--without-ensurepip
CONFIGURE_OPTIONS  +=		--enable-ipv6
CONFIGURE_OPTIONS  +=		--bindir=$(USRBINDIR)
# https://bugs.python.org/issue25003
# CONFIGURE_OPTIONS  +=		"ac_cv_func_getentropy=no"
CONFIGURE_OPTIONS  +=		CPPFLAGS="$(CPPFLAGS)"
CONFIGURE_OPTIONS  +=		LDFLAGS="$(LDFLAGS)"
CONFIGURE_OPTIONS  +=		CFLAGS="$(CFLAGS)"
CONFIGURE_OPTIONS  +=		DFLAGS="-$(BITS)"

COMPONENT_BUILD_ENV  +=		DFLAGS="-$(BITS)"

# Some tests have non-ASCII characters encoded for international domain names;
# the publish step will fail in 'pkgdepend generate' without this:
COMPONENT_PUBLISH_ENV  +=	LC_ALL=en_US.UTF-8

# parallel building of dtrace probes is not safe
COMPONENT_BUILD_ARGS =

# 64-bit shared objects need to go to 64-bit directory
COMPONENT_INSTALL_ARGS += DESTSHARED=$(CONFIGURE_PREFIX)/lib/python3.5/lib-dynload

build:		$(BUILD_64)

install:	$(INSTALL_64)

# Using "-uall,-network" ensures all tests are run except the network tests.
# The network tests contain many expected failures when run behind a firewall.
# The "-v" ensures verbose mode.  You can set TESTOPTS_PYTHON_TEST to a
# particular test if you want to run just one test.  For example,
# $ TESTOPTS_PYTHON_TEST=test_sys gmake -k test
# Note that when a test succeeds, the builds/*/.tested file gets created.  You
# may need to remove these files, or run "gmake clobber" or "gmake clean"
# between tests.
#
COMPONENT_TEST_ENV = EXTRATESTOPTS="-v -uall,-network $(TESTOPTS_PYTHON_TEST)"
# Prevent the tests from getting stuck waiting for input.
COMPONENT_TEST_TARGETS = test < /dev/null

# The test output contains details from each test, in whatever order they
# complete.  The default _TRANSFORMER is not powerful enough to deal with
# this; we need heavier artillery.  Extract just the sections that start
# with "tests OK." and end with "Re-running failed tests..." for comparison.
COMPONENT_TEST_TRANSFORMER =	$(NAWK)
COMPONENT_TEST_TRANSFORMS = "'/tests OK/ { results = 1 }; /^Re-running failed tests in verbose mode/ { results = 0 } { if (results) print }'"

test:		$(TEST_64)

# Required for dump(1)
REQUIRED_PACKAGES += developer/object-file
# Auto-generated dependencies
REQUIRED_PACKAGES += compress/bzip2
REQUIRED_PACKAGES += compress/xz
REQUIRED_PACKAGES += database/sqlite-3
REQUIRED_PACKAGES += library/database/gdbm
REQUIRED_PACKAGES += library/expat
REQUIRED_PACKAGES += library/libffi
REQUIRED_PACKAGES += library/ncurses
REQUIRED_PACKAGES += library/readline
REQUIRED_PACKAGES += library/security/openssl
REQUIRED_PACKAGES += library/zlib
REQUIRED_PACKAGES += runtime/tcl-8
REQUIRED_PACKAGES += runtime/tk-8
REQUIRED_PACKAGES += system/library
REQUIRED_PACKAGES += system/library/math
