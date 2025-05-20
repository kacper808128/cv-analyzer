import React, { useState } from 'react';
import '../styles/FileUploadForm.css';

interface FileUploadFormProps {
  onSubmit: (cvFile: File, jobDescFile: File) => void;
  isLoading: boolean;
}

const FileUploadForm: React.FC<FileUploadFormProps> = ({ onSubmit, isLoading }) => {
  const [cvFile, setCvFile] = useState<File | null>(null);
  const [jobDescFile, setJobDescFile] = useState<File | null>(null);
  const [cvError, setCvError] = useState<string>('');
  const [jobDescError, setJobDescError] = useState<string>('');

  // Dozwolone rozszerzenia plików
  const allowedExtensions = ['pdf', 'docx', 'txt'];

  // Funkcja walidująca plik
  const validateFile = (file: File): boolean => {
    const extension = file.name.split('.').pop()?.toLowerCase() || '';
    
    if (!allowedExtensions.includes(extension)) {
      return false;
    }
    
    // Maksymalny rozmiar pliku: 10MB
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
      return false;
    }
    
    return true;
  };

  // Obsługa zmiany pliku CV
  const handleCvFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      const file = files[0];
      
      if (!validateFile(file)) {
        setCvError('Nieprawidłowy format pliku. Dozwolone formaty: PDF, DOCX, TXT (max 10MB)');
        setCvFile(null);
      } else {
        setCvError('');
        setCvFile(file);
      }
    }
  };

  // Obsługa zmiany pliku ogłoszenia o pracę
  const handleJobDescFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      const file = files[0];
      
      if (!validateFile(file)) {
        setJobDescError('Nieprawidłowy format pliku. Dozwolone formaty: PDF, DOCX, TXT (max 10MB)');
        setJobDescFile(null);
      } else {
        setJobDescError('');
        setJobDescFile(file);
      }
    }
  };

  // Obsługa wysłania formularza
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!cvFile) {
      setCvError('Proszę wybrać plik CV');
      return;
    }
    
    if (!jobDescFile) {
      setJobDescError('Proszę wybrać plik ogłoszenia o pracę');
      return;
    }
    
    onSubmit(cvFile, jobDescFile);
  };

  return (
    <div className="file-upload-container">
      <h2>Analiza CV pod kątem zgodności z ogłoszeniem o pracę</h2>
      <p className="description">
        Prześlij swoje CV oraz ogłoszenie o pracę, aby sprawdzić poziom dopasowania i otrzymać szczegółową analizę.
      </p>
      
      <form onSubmit={handleSubmit} className="upload-form">
        <div className="file-input-group">
          <label htmlFor="cv-file" className="file-label">
            <div className="file-icon">
              <i className="document-icon"></i>
            </div>
            <div className="file-info">
              <span className="file-title">CV</span>
              <span className="file-description">Przeciągnij i upuść plik lub kliknij, aby wybrać</span>
              <span className="file-formats">Obsługiwane formaty: PDF, DOCX, TXT</span>
            </div>
          </label>
          <input
            type="file"
            id="cv-file"
            accept=".pdf,.docx,.txt"
            onChange={handleCvFileChange}
            className="file-input"
          />
          {cvFile && (
            <div className="selected-file">
              <span className="file-name">{cvFile.name}</span>
              <button
                type="button"
                className="remove-file"
                onClick={() => setCvFile(null)}
              >
                Usuń
              </button>
            </div>
          )}
          {cvError && <div className="error-message">{cvError}</div>}
        </div>

        <div className="file-input-group">
          <label htmlFor="job-desc-file" className="file-label">
            <div className="file-icon">
              <i className="document-icon"></i>
            </div>
            <div className="file-info">
              <span className="file-title">Ogłoszenie o pracę</span>
              <span className="file-description">Przeciągnij i upuść plik lub kliknij, aby wybrać</span>
              <span className="file-formats">Obsługiwane formaty: PDF, DOCX, TXT</span>
            </div>
          </label>
          <input
            type="file"
            id="job-desc-file"
            accept=".pdf,.docx,.txt"
            onChange={handleJobDescFileChange}
            className="file-input"
          />
          {jobDescFile && (
            <div className="selected-file">
              <span className="file-name">{jobDescFile.name}</span>
              <button
                type="button"
                className="remove-file"
                onClick={() => setJobDescFile(null)}
              >
                Usuń
              </button>
            </div>
          )}
          {jobDescError && <div className="error-message">{jobDescError}</div>}
        </div>

        <button
          type="submit"
          className="submit-button"
          disabled={isLoading || !cvFile || !jobDescFile}
        >
          {isLoading ? 'Analizowanie...' : 'Analizuj dopasowanie'}
        </button>
      </form>
    </div>
  );
};

export default FileUploadForm;
