#
# This file and its contents are supplied under the terms of the
# Common Development and Distribution License ("CDDL"), version 1.0.
# You may only use this file in accordance with the terms of version
# 1.0 of the CDDL.
#
# A full copy of the text of the CDDL should have accompanied this
# source.  A copy of the CDDL is also available via the Internet at
# http://www.illumos.org/license/CDDL.
#

#
# Copyright (c) 2017, 2018, Oracle and/or its affiliates. All rights reserved.
# Copyright 2018 Aurelien Larcher
#
BUILD_STYLE= archive

include ../../../make-rules/shared-macros.mk

COMPONENT_NAME=		arphic-ukai
COMPONENT_VERSION=	0.2.20080216.1
COMPONENT_REVISION=     1
COMPONENT_SUMMARY=	CJK Unicode TrueType font Ming style
COMPONENT_PROJECT_URL=	https://www.freedesktop.org/wiki/Software/CJKUnifonts
COMPONENT_SRC=		$(COMPONENT_NAME)-$(COMPONENT_VERSION)
COMPONENT_ARCHIVE=	$(COMPONENT_SRC).tar.gz
COMPONENT_ARCHIVE_URL= \
  http://archive.debian.org/debian/pool/main/t/ttf-$(COMPONENT_NAME)/ttf-$(COMPONENT_NAME)_$(COMPONENT_VERSION).orig.tar.gz
COMPONENT_ARCHIVE_HASH= \
  sha256:0ea93b3efdd3bb71026bc545479e34ce14263a9faa20e1ac124bcf7315d19f4a
# Archive does not contain any top directory
UNPACK_ARGS= -r $(COMPONENT_SRC)
COMPONENT_LICENSE=      ARPHIC PUBLIC LICENSE

FONT_TYPE= TTF

include $(WS_MAKE_RULES)/font.mk

COMPONENT_FONT_SRC_DIR     =
COMPONENT_FONT_FILES      += ukai.ttc
COMPONENT_FONTCONF_SRC_DIR =

