# srtc

Server Response Time Compare

# What is it

Simple tool to compare response times between two servers. It will launch 1000 requests to both endpoinds with parallelism set to 32. It will then plot the results and print out the average response time for each server including errors and percentage difference between both endpoints.

You can change request count in the `srtc.py` `TOTAL_REQUESTS_PER_URL = 1000` and parallelism in `srtc.py` `CONCURRENT_REQUESTS_PER_URL = 32`.

![srtc comparison graph](comparison_graph.png 'srtc comparison graph')

# Use case

If you need to check two servers and compare response times, this tool is for you. Also would work great to check two different versions of the same server.

Let's say you have two AWS lambdas and you want to determine how much memory it should use. With this tool you will be able to test both lambdas until you hit diminishing returns and choose the one that is the most cost effective.

# Requirements

Python libraries: `aiohttp`, `matplotlib`, `tqdm`.

`pip3 install aiohttp matplotlib tqdm`

# Usage

`python3 srtc.py https://stanislavromanov.com https://stanislavromanov.com/angular-consulting/`

# License

MIT License

Copyright (c) github.com/stanislavromanov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
