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

---

### pydantic-to-typescript

[pypi: pydantic-to-typescript 2.0.0](https://pypi.org/project/pydantic-to-typescript/)  
[npm: json-schema-to-typescript](https://www.npmjs.com/package/json-schema-to-typescript)

```
cd ~/MRCSMacProject/mrcs-api
```

```
pydantic2ts --module src/mrcs_api/models/message.py --output frontend/message.ts;
pydantic2ts --module src/mrcs_api/models/time.py --output frontend/time.ts;
pydantic2ts --module src/mrcs_api/models/token.py --output frontend/token.ts;
pydantic2ts --module src/mrcs_api/models/user.py --output frontend/user.ts;
```

