#!/bin/bash

LOG_FILE="clarknet_access_log_Sep4"

echo "================== Log File Analysis Report =================="
echo "Log File: $LOG_FILE"
echo

# 1. Total number of requests
echo "1. Total requests: $(wc -l < "$LOG_FILE")"

# 2. GET requests
echo "2. Total GET requests: $(grep '\"GET' "$LOG_FILE" | wc -l)"

# 3. POST requests
echo "3. Total POST requests: $(grep '\"POST' "$LOG_FILE" | wc -l)"

# 4. Unique IP addresses
echo "4. Unique IP addresses: $(awk '{print $1}' "$LOG_FILE" | sort | uniq | wc -l)"

# 5. Requests per IP - GET and POST
echo "5. Requests per IP (GET and POST):"
awk '{print $1, $6}' "$LOG_FILE" | grep -E '"GET|POST' | awk '{print $1, $2}' | sort | uniq -c | sort -nr | head

# 6. Failed requests
echo "6. Failed requests : $(awk '$9 ~ /^[45]/' "$LOG_FILE" | wc -l)"

# 7. Failure percentage
total=$(wc -l < "$LOG_FILE")
fail=$(awk '$9 ~ /^[45]/' "$LOG_FILE" | wc -l)
fail_percent=$(awk "BEGIN {printf \"%.2f\", ($fail/$total)*100}")
echo "7. Failure percentage: $fail_percent%"

# 8. Most active IP
echo "8. Most active IP:"
awk '{print $1}' "$LOG_FILE" | sort | uniq -c | sort -nr | head -1

# 9. Requests per day
echo "9. Requests per day:"
awk -F: '{print $1}' "$LOG_FILE" | awk '{gsub(/\[/, "", $4); print $4}' | sort | uniq -c

# 10. Daily average requests:
echo -n "10. Average requests per day: "
awk -F: '{print $1}' "$LOG_FILE" | awk '{gsub(/\[/, "", $4); print $4}' | sort | uniq -c | awk '{sum+=$1; count++} END {print int(sum/count)}'

# 11. Failure per day
echo "11. Days with highest failures:"
awk '$9 ~ /^[45]/ {split($4,a,":"); gsub(/\[/, "", a[1]); print a[1]}' "$LOG_FILE" | sort | uniq -c | sort -nr | head

# 12. Requests per hour
echo "12. Requests per hour:"
awk -F: '{print $2}' "$LOG_FILE" | sort | uniq -c

# 13. Status code breakdown
echo "13. Status code breakdown:"
awk '{print $9}' "$LOG_FILE" | sort | uniq -c | sort -nr

# 14. Most active IP - GET
echo "14. Most active IP with GET:"
grep '\"GET' "$LOG_FILE" | awk '{print $1}' | sort | uniq -c | sort -nr | head -1

# 15. Most active IP - POST
echo "15. Most active IP with POST:"
grep '\"POST' "$LOG_FILE" | awk '{print $1}' | sort | uniq -c | sort -nr | head -1

# 16. Most requested pages
echo "16. Most requested pages:"
awk '{print $7}' "$LOG_FILE" | sort | uniq -c | sort -nr | head

# 17. 404 Errors Count
echo "17. Total 404 errors: $(awk '$9 == 404' "$LOG_FILE" | wc -l)"

# 18. Top pages with 404:
echo "18. Top 404 pages:"
awk '$9 == 404 {print $7}' "$LOG_FILE" | sort | uniq -c | sort -nr | head

# 19. High traffic IPs in same hour
echo "19. IPs with over 100 requests in same hour:"
awk '{split($4,t,":"); print $1" "t[1]":"t[2]}' "$LOG_FILE" | sort | uniq -c | awk '$1 > 100'

# 20. IPs with only failed requests
echo "20. IPs with only 4xx/5xx requests:"
awk '$9 ~ /^[45]/ {print $1}' "$LOG_FILE" | sort | uniq -c | sort -nr | head

# 21. Requests by file type 
echo "21. Requests by file type:"
awk '{print $7}' "$LOG_FILE" | grep -oE '\.[a-z]+$' | sort | uniq -c | sort -nr


# 22. Count of HEAD requests
echo "23. Total HEAD requests: $(grep '\"HEAD' "$LOG_FILE" | wc -l)"

# 23. Bytes transferred - if column 10 has byte size
echo "24. Total bytes transferred:"
awk '{s+=$10} END {print s}' "$LOG_FILE"

# 24. Average bytes per request
echo -n "25. Average bytes/request: "
awk '{s+=$10; c++} END {print int(s/c)}' "$LOG_FILE"

echo "==================================================="
