import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import eltTemplateService from '../service/EltTemplateService';
import { Link } from "react-router-dom";
import api from '../service/api';
import { useTranslation } from "react-i18next";
import { Alert, Modal, Button, Table, InputGroup, Form } from 'react-bootstrap';

function WorkerList() {
  const { t } = useTranslation();
  const dispatch = useDispatch();
  const [newTemplateModal, setNewTemplateModal] = useState(false);
  const [templateName, setTemplateName] = useState("templateName");

  const workers = useSelector((state: any) => state.workers.workers)

  useEffect(() => {
    dispatch(eltTemplateService.getWorkers());
  }, []);


  const downloadEltTmplate = (name: string) => {
    api.get('/elttemplates/' + name).then(response => {
      let url = window.URL.createObjectURL(new Blob([JSON.stringify(response.data, null, 2)], { type: "application/json" }));
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = response.data.name + ".json";
      a.click();
      window.URL.revokeObjectURL(url);
      a.remove();
    }).catch(error => {
      alert(error.message);
    })
  }
  const createNewTemplate = () => {
	eltTemplateService.newEltTemplate(templateName);
    dispatch(eltTemplateService.getWorkers());
  }
  return (
    <div>
      <br/>
      <Button variant="primary" onClick={() => setNewTemplateModal(true)}><i className="bi bi-plus-square"></i> {t("New element template")}</Button>
      <Alert variant="info">The following list contains workers that were automatically detected at runtime. You can define element templates on top of these workers to provide guided properties at conception time for your business stakeholders.</Alert>
      <Table striped bordered hover>
        <tbody>
          {workers ? workers.map((worker: string, index: number) =>
            <tr key={index}>
              <td>{worker}</td>
              <td>

                <Button variant="primary" className="me-1" onClick={() => downloadEltTmplate(worker)}><i className="bi bi-download"> </i> {t("Element template")}</Button>
                <Link className="btn btn-primary" to={"/admin/elementTemplate/" + worker}><i className="bi bi-pencil"> </i> {t("Edit template")}</Link>
                     
              </td>
            </tr>)
          : <></>}
		</tbody>
      </Table>
	  
      <Modal show={newTemplateModal} onHide={() => setNewTemplateModal(false)} >
        <Modal.Header closeButton>
          <Modal.Title>New element template</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <InputGroup className="mb-3">
            <InputGroup.Text>Template name</InputGroup.Text>
            <Form.Control placeholder="template name" value={templateName} onChange={(evt) => setTemplateName(evt.target.value)} />
          </InputGroup>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="primary" onClick={createNewTemplate}>Create</Button>
          <Button variant="secondary" onClick={() => setNewTemplateModal(false)}> Close</Button>
        </Modal.Footer>
      </Modal>
  </div >
  );
}

export default WorkerList;
