# Base image
FROM ruby

# Install bundler
RUN gem install bundler

# Set working directory
WORKDIR /usr/src/app

# Copy Gemfile and Gemfile.lock first (for caching)
COPY Gemfile /usr/src/app/

# Install project dependencies
RUN bundle install