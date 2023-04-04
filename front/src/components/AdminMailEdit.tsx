import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import adminMailService from '../service/AdminMailService';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import CodeMirror from '@uiw/react-codemirror';
import { html } from '@codemirror/lang-html';
import { json } from '@codemirror/lang-json';
import { useTranslation } from "react-i18next";

function AdminMailEdit() {
  const { t } = useTranslation();
  const dispatch = useDispatch();
  const [preview, setPreview] = useState<string>('');

  const mail = adminMailService.getCurrentMail();

  const loadPreview = async () => {
    let data:string = await adminMailService.preview();
    setPreview(data);
  }

  const onChange = React.useCallback((value: string, viewUpdate: any) => {
    dispatch(adminMailService.setMailTemplate(value));
    loadPreview();
  }, []);
  const onChangePreviewData = React.useCallback((value: string, viewUpdate: any) => {
    dispatch(adminMailService.setMailPreviewData(JSON.parse(value)));
    loadPreview();
  }, []);

  useEffect(() => {
    loadPreview();
  }, []);

  return (
    <Row className="maileditor">
      <Col className="card">
        <h5 className="card-title bg-primary text-light">{t("Mail editor")}</h5>
        <CodeMirror
          value={mail.htmlTemplate}
          extensions={[html()]}
          onChange={onChange}/>
      </Col>
      <Col >
        <div className="card" style={{ height: 'calc(80vh - 145px)' }}>
          <h5 className="card-title bg-primary text-light">{t("Mail preview")}</h5>
          <div dangerouslySetInnerHTML={{ __html: preview }}></div>
        </div>

        <div className="card" style={{ height: '20vh' }} >
          <span className="card-title bg-primary text-light">Data preview value</span>
          <CodeMirror
            value={JSON.stringify(mail.previewData)}
            extensions={[json()]}
            onChange={onChangePreviewData}
          />
        </div>
      </Col>

    </Row>
  );
}

export default AdminMailEdit
