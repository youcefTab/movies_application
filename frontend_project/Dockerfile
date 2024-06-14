FROM node:lts-alpine

# Set the working directory in the container to /app
WORKDIR /app

# Install Yarn
RUN npm install yarn

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./
COPY yarn.lock ./

# Install any needed dependencies
RUN yarn install

# Copy the rest of the application code to the working directory
COPY . .

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Run the app when the container launches
CMD ["yarn", "serve", "--port", "3000"]