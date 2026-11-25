#!/bin/bash
echo "=========================================================="
echo " Starting Cloudflare High-Speed Public Tunnel..."
echo "=========================================================="
/Users/bindanm/IndicSent-M/bin/cloudflared tunnel --url http://127.0.0.1:8000
