# Step 1: Use an official Node.js image as the base image
FROM node:18-alpine as build

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy package.json and package-lock.json (or yarn.lock) into the container
COPY package.json package-lock.json ./

# Step 4: Install app dependencies
RUN npm install

# Step 5: Copy the rest of the application code
COPY . .

# Step 6: Expose port 5173 for the React app
EXPOSE 5173

# Step 7: Run the app in development mode using Vite
CMD ["npm", "run", "dev"]
