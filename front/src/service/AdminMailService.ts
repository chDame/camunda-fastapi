import store, { AppThunk } from '../store';
import { loadStart, loadSuccess, setCurrentMail, setHtmlTemplate, setPreviewData, setMailName, fail, silentfail } from '../store/features/adminMails/slice';
import api from './api';

export class AdminMailService {
  lastFetch: number = 0;
  getDefaultMail = (): any => {
    return {
      name: 'NewMail-en',
      htmlTemplate: `<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:th="http://www.thymeleaf.org">
<head>
</head>
<body>
  <div class="header"></div>
  <p>Hello {{firstname}}</p>
  <p>This is an example mail template generated by {{generator}}.</p>
  <p>Sincerely,</p>
  <p>Your camunda presales team</p>
  <p><img src="https://camunda.com/wp-content/uploads/camunda/blog-images/4-icon.png" style="width:50px;"/></p>
</body>
</html>`,
      previewData:{"firstname":"Chris","generator":"Chevron"}
    }
  }
  geMails = (): AppThunk => async dispatch => {
    if (this.lastFetch < Date.now() - 5000) { 
      try {
        dispatch(loadStart());
        const { data } = await api.get<string[]>('/edition/mails/names');
        dispatch(loadSuccess(data));
      } catch(error: any) {
        if (error.response) {
          // The request was made. server responded out of range of 2xx
          dispatch(fail(error.response.data.message));
        } else if (error.request) {
          // The request was made but no response was received
          dispatch(fail('ERROR_NETWORK'));
        } else {
          // Something happened in setting up the request that triggered an Error
          console.warn('Error', error.message);
          dispatch(fail(error.toString()));
        }
      }
      this.lastFetch = Date.now();
    }
  }
  newMail = (): AppThunk => async dispatch => {
    dispatch(setCurrentMail(this.getDefaultMail()));
  }
  openMail = (name:string): AppThunk => async dispatch => {
    api.get('/edition/mails/' + name).then(response => {
      dispatch(setCurrentMail(response.data));
    }).catch(error => {
      alert(error.message);
    })
  }
  deleteMail = (name: string): AppThunk => async dispatch => {
    api.delete('/edition/mails/' + name).then(response => {
      dispatch(this.geMails());
    }).catch(error => {
      alert(error.message);
    })
  }
  setMail = (mail: any): AppThunk => async dispatch => {
    dispatch(setCurrentMail(mail));
  }
  setMailTemplate = (htmlTemplate: string): AppThunk => async dispatch => {
    dispatch(setHtmlTemplate(htmlTemplate));
  }
  setMailPreviewData = (data: string): AppThunk => async dispatch => {
    dispatch(setPreviewData(data));
  }
  setMailName = (mailName: string): AppThunk => async dispatch => {
    dispatch(setMailName(mailName));
  }
  saveCurrentMail = (): AppThunk => async dispatch => {
    let mail = Object.assign({}, store.getState().adminMails.currentMail);
    api.post('/edition/mails', mail).then(response => {
      dispatch(setCurrentMail(response.data));
    }).catch(error => {
      alert(error.message);
    })
  }

  preview = async(): Promise<string> => {
    const { data } = await api.post('/edition/mails/preview', store.getState().adminMails.currentMail);
    return data;
  }
  getCurrentMail = (): any => {
    return store.getState().adminMails.currentMail;
  }
}

const adminMailService = new AdminMailService();

export default adminMailService;
