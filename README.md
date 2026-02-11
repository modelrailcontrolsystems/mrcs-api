# mrcs-api

_Application Programming Interfaces (APIs) for the Model Rail Control Systems (MRCS) domain_

---

### Repos

Requires MRCS repos:

* **[mrcs-control](https://github.com/modelrailcontrolsystems/mrcs-core)**
* **[mrcs-core](https://github.com/modelrailcontrolsystems/mrcs-core)**

---

### Services

The following services should be running continuously:

* `mrcs_uvicorn --verbose --reload --test &`

---

### URLs

API root:  
http://localhost:8000/

API Swagger docs:  
http://localhost:8000/docs

WebSocket test page:  
http://localhost:8000/ws
