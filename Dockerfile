# Builder stage
FROM python:3.9-alpine as builder

# A few Utilities to able to install C based libraries such as numpy
RUN apk update
RUN apk add make automake gcc g++ git

# Copy the project files into the builder container
COPY . .

# Install the project dependencies and build the package
RUN make dist

# Actual container
FROM python:3.9-alpine

# Copy the built package from the builder stage
COPY --from=builder /dist/*.whl /tmp/

# Install the package
RUN pip install /tmp/*.whl

CMD filet
