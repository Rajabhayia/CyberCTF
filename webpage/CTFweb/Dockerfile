# Use node:alpine as a base image for React
FROM node:18-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json /app/
RUN npm install

# Copy all the React app files into the container
COPY . /app/

# Expose the port where the Vite server will run
EXPOSE 5173

# Start the React development server
CMD ["npm", "run", "dev"]
