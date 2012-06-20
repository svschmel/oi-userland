/*
 * Copyright (c) 2003, 2012, Oracle and/or its affiliates. All rights reserved.
 *
 * U.S. Government Rights - Commercial software. Government users are subject
 * to the Sun Microsystems, Inc. standard license agreement and applicable
 * provisions of the FAR and its supplements.
 *
 *
 * This distribution may include materials developed by third parties. Sun,
 * Sun Microsystems, the Sun logo and Solaris are trademarks or registered
 * trademarks of Sun Microsystems, Inc. in the U.S. and other countries.
 *
 */
/*
 * Note: this file originally auto-generated by mib2c using
 *         : mib2c.scalar.conf,v 1.5 2002/07/18 14:18:52 dts12 Exp $
 */
#include <sys/systeminfo.h>

#include <net-snmp/net-snmp-config.h>
#include <net-snmp/net-snmp-includes.h>
#include <net-snmp/agent/net-snmp-agent-includes.h>
#include "sunSystem.h"

/* Initializes the sunSystem module */
void
init_sunSystem(void)
{
    static oid motd_oid[] = { 1, 3, 6, 1, 4, 1, 42, 3, 1, 3,  0 };
    static oid hostID_oid[] = { 1, 3, 6, 1, 4, 1, 42, 3, 1, 2,  0 };
    static oid agentDescr_oid[] = { 1, 3, 6, 1, 4, 1, 42, 3, 1, 1,  0 };
    static oid unixTime_oid[] = { 1, 3, 6, 1, 4, 1, 42, 3, 1, 4,  0 };

    DEBUGMSGTL(("sunSystem", "Initializing\n"));

    netsnmp_register_read_only_instance(netsnmp_create_handler_registration
                                    ("motd",
                                    get_motd,
                                    motd_oid,
                                    OID_LENGTH(motd_oid),
                                    HANDLER_CAN_RONLY));
    netsnmp_register_read_only_instance(netsnmp_create_handler_registration
                                    ("hostID",
                                    get_hostID,
                                    hostID_oid,
                                    OID_LENGTH(hostID_oid),
                                    HANDLER_CAN_RONLY));
    netsnmp_register_read_only_instance(netsnmp_create_handler_registration
                                    ("agentDescr",
                                    get_agentDescr,
                                    agentDescr_oid,
                                    OID_LENGTH(agentDescr_oid),
                                    HANDLER_CAN_RONLY));
    netsnmp_register_read_only_instance(netsnmp_create_handler_registration
                                    ("unixTime",
                                    get_unixTime,
                                    unixTime_oid,
                                    OID_LENGTH(unixTime_oid),
                                    HANDLER_CAN_RONLY));
}

int
get_motd(netsnmp_mib_handler *handler,
         netsnmp_handler_registration *reginfo,
         netsnmp_agent_request_info *reqinfo,
         netsnmp_request_info *requests)
{
    static char motd[256];
    FILE *fd;

    /*
     * We are never called for a GETNEXT if it's registered as a
     * "instance", as it's "magically" handled for us.
     */

    /*
     * a instance handler also only hands us one request at a time, so
     * we don't need to loop over a list of requests; we'll only get one.
     */

    switch (reqinfo->mode) {

    case MODE_GET:
        motd[0] = '\0';
        fd = fopen("/etc/motd", "r");

	if (fd != NULL) {
	    fgets(motd, sizeof (motd), fd);
	    fclose(fd);
	}

        snmp_set_var_typed_value(requests->requestvb, ASN_OCTET_STR,
                                (u_char *) motd, strlen(motd));
        break;

    default:
        /* we should never get here, so this is a really bad error */
        return (SNMP_ERR_GENERR);
    }

    return (SNMP_ERR_NOERROR);
}

int
get_hostID(netsnmp_mib_handler *handler,
           netsnmp_handler_registration *reginfo,
           netsnmp_agent_request_info *reqinfo,
           netsnmp_request_info *requests)
{
    static unsigned int int_my_host_id;
    static unsigned long int my_host_id;
    char sibuf[16];

    /*
     * We are never called for a GETNEXT if it's registered as a
     * "instance", as it's "magically" handled for us.
     */

    /*
     * a instance handler also only hands us one request at a time, so
     * we don't need to loop over a list of requests; we'll only get one.
     */

    switch (reqinfo->mode) {

    case MODE_GET:
        (void) sysinfo(SI_HW_SERIAL, sibuf, (long) sizeof (sibuf));
        my_host_id = atol(sibuf);

        if (sizeof(my_host_id) == sizeof(int)) {
            snmp_set_var_typed_value(requests->requestvb, ASN_OCTET_STR,
                                     (u_char *) &my_host_id,
                                     sizeof (my_host_id));
        } else {
            int_my_host_id = (u_int)my_host_id;
            snmp_set_var_typed_value(requests->requestvb, ASN_OCTET_STR,
                                     (u_char *) &int_my_host_id,
                                     sizeof (int_my_host_id));
        }
        break;


    default:
        /* we should never get here, so this is a really bad error */
        return (SNMP_ERR_GENERR);
    }

    return (SNMP_ERR_NOERROR);
}

int
get_agentDescr(netsnmp_mib_handler *handler,
               netsnmp_handler_registration *reginfo,
               netsnmp_agent_request_info *reqinfo,
               netsnmp_request_info *requests)
{
    /*
     * We are never called for a GETNEXT if it's registered as a
     * "instance", as it's "magically" handled for us.
     */

    /*
     * a instance handler also only hands us one request at a time, so
     * we don't need to loop over a list of requests; we'll only get one.
     */

    switch (reqinfo->mode) {

    case MODE_GET:
        snmp_set_var_typed_value(requests->requestvb, ASN_OCTET_STR,
                    (u_char *) AGENT_DESCR, strlen(AGENT_DESCR));
        break;

    default:
        /* we should never get here, so this is a really bad error */
        return (SNMP_ERR_GENERR);
    }

    return (SNMP_ERR_NOERROR);
}

int
get_unixTime(netsnmp_mib_handler *handler,
             netsnmp_handler_registration *reginfo,
             netsnmp_agent_request_info *reqinfo,
             netsnmp_request_info *requests)
{
    struct timeval now_is;
    long now_is_tv_sec;

    /*
     * We are never called for a GETNEXT if it's registered as a
     * "instance", as it's "magically" handled for us.
     */

    /*
     * a instance handler also only hands us one request at a time, so
     * we don't need to loop over a list of requests; we'll only get one.
     */

    switch (reqinfo->mode) {

    case MODE_GET:
        (void) gettimeofday(&now_is, (struct timezone *)0);
        now_is_tv_sec = (long)now_is.tv_sec;
        snmp_set_var_typed_value(requests->requestvb, ASN_COUNTER,
                                 (u_char *) &now_is_tv_sec,
                                 sizeof (now_is_tv_sec));
        break;

    default:
        /* we should never get here, so this is a really bad error */
        return (SNMP_ERR_GENERR);
    }

    return (SNMP_ERR_NOERROR);
}
