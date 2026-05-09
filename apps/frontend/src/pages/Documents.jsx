import { useEffect, useState } from "react"
import API from "../services/api"
import toast from "react-hot-toast"

function Documents() {

  const [documents, setDocuments] = useState([])
  const [selectedFile, setSelectedFile] = useState(null)
  const [loading, setLoading] = useState(false)

  // FETCH DOCUMENTS
  const fetchDocuments = async () => {

    try {

      const token = localStorage.getItem("token")

      const response = await API.get(
        "/documents/",
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      setDocuments(response.data)

    } catch (error) {
      console.error(error)
    }
  }

  // LOAD ON PAGE OPEN
  useEffect(() => {
    fetchDocuments()
  }, [])

  // UPLOAD DOCUMENT
  const handleUpload = async () => {

    if (!selectedFile) {
      toast.error("Please select a file")
      return
    }

    try {

      setLoading(true)

      const formData = new FormData()
      formData.append("file", selectedFile)

      const token = localStorage.getItem("token")

      await API.post(
        "/ingestion/upload",
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data"
          }
        }
      )

      toast.success("Document uploaded successfully!")

      setSelectedFile(null)

      // REFRESH DOCUMENT LIST
      fetchDocuments()

    } catch (error) {

      console.error(error)

      toast.error("Upload failed")

    }

    setLoading(false)
  }

  // DELETE DOCUMENT
  const handleDelete = async (documentId) => {
  
    try {
    
      const token = localStorage.getItem("token")
    
      await API.delete(
        `/documents/${documentId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )
    
      // SUCCESS TOAST
      toast.success("Document deleted successfully!")
    
      // REMOVE FROM UI
      setDocuments((prev) =>
        prev.filter((doc) => doc.id !== documentId)
      )
    
    } catch (error) {
    
      console.error(error)
    
      toast.error("Delete failed")
    }
  }

  return (
    <div>

      {/* HEADER */}
      <div className="flex items-center justify-between mb-8">

        <div>
          <h1 className="text-5xl font-bold text-slate-900">
            Documents
          </h1>

          <p className="text-slate-500 mt-2">
            Upload and manage company knowledge documents
          </p>
        </div>

      </div>

      {/* UPLOAD BOX */}
      <div className="bg-white rounded-3xl p-10 shadow-sm border border-slate-200 mb-8">

        <div className="border-2 border-dashed border-slate-300 rounded-3xl p-14 text-center">

          <h2 className="text-2xl font-bold mb-4">
            Upload Document
          </h2>

          <p className="text-slate-500 mb-8">
            PDF, CSV, XLSX, EML
          </p>

          <div className="flex flex-col items-center gap-5">

            <input
              type="file"
              onChange={(e) => setSelectedFile(e.target.files[0])}
            />

            <button
              onClick={handleUpload}
              disabled={loading}
              className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-3 rounded-2xl transition"
            >
              {loading ? "Uploading..." : "Upload"}
            </button>

          </div>

        </div>

      </div>

      {/* DOCUMENT TABLE */}
      <div className="bg-white rounded-3xl shadow-sm overflow-hidden">

        <table className="w-full">

          <thead className="bg-slate-50 border-b border-slate-200">

            <tr>

              <th className="text-left px-6 py-5 text-sm font-semibold text-slate-700">
                Filename
              </th>

              <th className="text-left px-6 py-5 text-sm font-semibold text-slate-700">
                Type
              </th>

              <th className="text-left px-6 py-5 text-sm font-semibold text-slate-700">
                Uploaded By
              </th>

              <th className="text-left px-6 py-5 text-sm font-semibold text-slate-700">
                Actions
              </th>

            </tr>

          </thead>

          <tbody>

            {documents.map((doc) => (

              <tr
                key={doc.id}
                className="border-b border-slate-100 hover:bg-slate-50 transition"
              >

                <td className="px-6 py-5">
                  {doc.filename}
                </td>

                <td className="px-6 py-5 uppercase">
                  {doc.file_type}
                </td>

                <td className="px-6 py-5">
                  {doc.uploaded_by}
                </td>

                <td className="px-6 py-5">

                  <button
                    onClick={() => handleDelete(doc.id)}
                    className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-xl"
                  >
                    Delete
                  </button>

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>
  )
}

export default Documents