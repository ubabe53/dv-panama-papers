### Panama Papers Dashboard
Visualizing the panama papers; interactive dashboard about Mossack Fonseca leading firm in incorporation of offshore entities.

---

Initially we hosted it through heroku, but as it was free-tier has expired. So here are the steps to run it locally through docker. 

1. Clone the project locally 
  ```
  git clone https://github.com/ubabe53/dv-panama-papers.git
  ```
  

2. Build the docker image and run a container
  ```
  docker build -t panama-dashboard .
  ```
  ```
  docker run -dp 8000:5000 panama-dashboard
  ```

3. It should be available in your web browser at `http://localhost:8000/`
