#define _GNU_SOURCE

#include <arpa/inet.h>
#include <linux/if.h>
#include <linux/if_ether.h>
#include <netinet/ether.h>
#include <netinet/in.h>
#include <sys/ioctl.h>
#include <sys/socket.h>

#include <errno.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "MaxSLiCInterface.h"

int main(int argc, char *argv[]) {
	struct in_addr dfe_ip1;
	inet_aton("172.20.50.1", &dfe_ip1);
	struct in_addr netmask;
	inet_aton("255.255.255.0", &netmask);

	max_file_t *maxfile = PacketFilter_init();
	max_engine_t * engine = max_load(maxfile, "*");

	max_ip_config(engine, MAX_NET_CONNECTION_QSFP_TOP_10G_PORT1, &dfe_ip1, &netmask);
//	max_ip_config(engine, MAX_NET_CONNECTION_QSFP_BOT_10G_PORT1, &dfe_ip2, &netmask);



	max_config_set_bool(MAX_CONFIG_PRINTF_TO_STDOUT, true);

	max_actions_t *action = max_actions_init(maxfile, NULL);
//	max_set_uint64t(action, "echoKernel", "localIp", dfe_ip2.s_addr);
//	max_set_uint64t(action, "echoKernel", "forwardIp", remote_ip2.s_addr);
//	max_set_uint64t(action, "echoKernel", "localMac", localMac);
//	max_set_uint64t(action, "echoKernel", "forwardMac", forwardMac);
	max_run(engine, action);

	printf("DFE Running.\n");
	getchar();

	max_unload(engine);
	max_file_free(maxfile);

	printf("Done.\n");
	return 0;
}
