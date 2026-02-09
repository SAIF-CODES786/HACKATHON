import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, X } from 'lucide-react';

const UploadSection = ({ onUpload, uploadedFiles, setUploadedFiles, isLoading }) => {
    const onDrop = useCallback((acceptedFiles) => {
        setUploadedFiles(prev => [...prev, ...acceptedFiles]);
    }, [setUploadedFiles]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'application/pdf': ['.pdf'],
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
        },
        multiple: true
    });

    const removeFile = (index) => {
        setUploadedFiles(prev => prev.filter((_, i) => i !== index));
    };

    const handleUpload = () => {
        if (uploadedFiles.length > 0) {
            onUpload(uploadedFiles);
        }
    };

    return (
        <div className="card animate-fade-in">
            <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                <Upload className="w-6 h-6 text-primary-600" />
                Upload Resumes
            </h2>

            <div
                {...getRootProps()}
                className={`border-3 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all duration-300 ${isDragActive
                        ? 'border-primary-500 bg-primary-50'
                        : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
                    }`}
            >
                <input {...getInputProps()} />
                <Upload className={`w-16 h-16 mx-auto mb-4 ${isDragActive ? 'text-primary-600' : 'text-gray-400'}`} />
                {isDragActive ? (
                    <p className="text-lg text-primary-600 font-semibold">Drop the files here...</p>
                ) : (
                    <div>
                        <p className="text-lg text-gray-700 font-semibold mb-2">
                            Drag & drop resume files here, or click to select
                        </p>
                        <p className="text-sm text-gray-500">
                            Supports PDF and DOCX files
                        </p>
                    </div>
                )}
            </div>

            {uploadedFiles.length > 0 && (
                <div className="mt-6">
                    <h3 className="text-lg font-semibold text-gray-700 mb-3">
                        Selected Files ({uploadedFiles.length})
                    </h3>
                    <div className="space-y-2 max-h-64 overflow-y-auto">
                        {uploadedFiles.map((file, index) => (
                            <div
                                key={index}
                                className="flex items-center justify-between bg-gray-50 p-3 rounded-lg hover:bg-gray-100 transition-colors"
                            >
                                <div className="flex items-center gap-3">
                                    <FileText className="w-5 h-5 text-primary-600" />
                                    <div>
                                        <p className="text-sm font-medium text-gray-800">{file.name}</p>
                                        <p className="text-xs text-gray-500">
                                            {(file.size / 1024).toFixed(2)} KB
                                        </p>
                                    </div>
                                </div>
                                <button
                                    onClick={() => removeFile(index)}
                                    className="text-red-500 hover:text-red-700 transition-colors"
                                >
                                    <X className="w-5 h-5" />
                                </button>
                            </div>
                        ))}
                    </div>

                    <button
                        onClick={handleUpload}
                        disabled={isLoading}
                        className="btn-primary w-full mt-4 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {isLoading ? (
                            <span className="flex items-center justify-center gap-2">
                                <div className="w-5 h-5 border-3 border-white border-t-transparent rounded-full animate-spin"></div>
                                Processing...
                            </span>
                        ) : (
                            `Upload ${uploadedFiles.length} Resume${uploadedFiles.length > 1 ? 's' : ''}`
                        )}
                    </button>
                </div>
            )}
        </div>
    );
};

export default UploadSection;
