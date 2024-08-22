import React from 'react';
import ReactDOM from 'react-dom';

// Modal Component for General Results
const ResultModal = ({ isOpen, onClose, message, score }) => {
  if (!isOpen) return null;

  return ReactDOM.createPortal(
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white p-6 rounded-lg shadow-lg max-w-sm mx-auto">
        <h2 className="text-lg font-bold">Game Result</h2>
        <p className="mt-2">{message}</p>
        {score && <p className="mt-2 text-xl font-bold">{score}</p>}
        <div className="flex justify-end mt-4">
          <button
            className="bg-blue-500 text-white px-4 py-2 rounded-lg"
            onClick={onClose}
          >
            OK
          </button>
        </div>
      </div>
    </div>,
    document.body
  );
};

// Modal Component for Resignation Confirmation
const ConfirmationModal = ({ isOpen, onClose, onConfirm }) => {
  if (!isOpen) return null;

  return ReactDOM.createPortal(
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white p-6 rounded-lg shadow-lg max-w-sm mx-auto">
        <h2 className="text-lg font-bold">Confirm Resignation</h2>
        <p className="mt-2">Are you sure you want to resign?</p>
        <div className="flex justify-end mt-4">
          <button
            className="bg-gray-500 text-white px-4 py-2 rounded-lg mr-2"
            onClick={onClose}
          >
            No
          </button>
          <button
            className="bg-red-500 text-white px-4 py-2 rounded-lg"
            onClick={onConfirm}
          >
            Yes
          </button>
        </div>
      </div>
    </div>,
    document.body
  );
};

export { ResultModal, ConfirmationModal };
