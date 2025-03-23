import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Table, Button, Form } from "react-bootstrap";
import ReactPaginate from "react-paginate";

const AdminDashboard = () => {
  const [images, setImages] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const [editImageId, setEditImageId] = useState(null);
  const [editUserId, setEditUserId] = useState(null);
  const [editImageData, setEditImageData] = useState({});
  const [editUserData, setEditUserData] = useState({});
  const [selectedImage, setSelectedImage] = useState(null);
  const [currentPage, setCurrentPage] = useState(0);
  const imagesPerPage = 5;

  useEffect(() => {
    const token = JSON.parse(localStorage.getItem("user"))?.token;
    const role = JSON.parse(localStorage.getItem("user"))?.role;
    if (role !== "admin") navigate("/");
    if (token) {
      fetchImages(token);
      fetchUsers(token);
    } else navigate("/login");
  }, [navigate]);


  const handleImageChange = (e) => {
    setSelectedImage(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedImage) {
      alert("Please select an image to upload.");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("image", selectedImage);

    const token = JSON.parse(localStorage.getItem("user"))?.token;

    try {
      // Upload the image and predict the location
      const response = await fetch("http://127.0.0.1:8000/api/predict-location/", {
        method: "POST",
        body: formData,
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to upload image and predict location");
      }

      const data = await response.json();

      // Assuming the backend returns the image with predicted location
      const { location, latitude, longitude, distance, cost } = data; // Backend response
      setImages([
        ...images,
        { location, latitude, longitude, distance, cost, image_url: data.image_url }, // Assuming image_url is returned
      ]);

      alert("Image uploaded and location predicted successfully!");
    } catch (error) {
      alert(error.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchImages = async (token) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/image-locations/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await response.json();
      setImages(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const fetchUsers = async (token) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/users/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await response.json();
      setUsers(data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleDeleteImage = async (id) => {
    const token = JSON.parse(localStorage.getItem("user"))?.token;
    try {
      await fetch(`http://127.0.0.1:8000/api/image-location/${id}/delete/`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchImages(token);
    } catch (error) {
      console.error(error);
    }
  };


  const handleEditImage = (image) => {
    setEditImageId(image.id);
    setEditImageData(image);
  };


  const handleSaveImage = async () => {
    const token = JSON.parse(localStorage.getItem("user"))?.token;
  
    const formData = new FormData();
    formData.append("location", editImageData.location);
    formData.append("latitude", editImageData.latitude);
    formData.append("longitude", editImageData.longitude);
    formData.append("cost", editImageData.cost);
    formData.append("distance", editImageData.distance);
    
    // Check if a new file was selected
    if (editImageData.image instanceof File) {
      formData.append("image", editImageData.image);  // Append file correctly
    }
  
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/image-location/${editImageId}/update/`, {
        method: "PUT",
        headers: {
          "Authorization": `Bearer ${token}`
        },
        body: formData,  // Send as FormData, NOT JSON
      });
  
      const responseData = await response.json();
  
      if (!response.ok) {
        console.error("Error updating image:", responseData);
      } else {
        console.log("Image updated successfully:", responseData);
        fetchImages(token);
        setEditImageId(null);
      }
    } catch (error) {
      console.error("Network error:", error);
    }
  };
  

  const handleSaveUser = async () => {
    const token = JSON.parse(localStorage.getItem("user"))?.token;
  
    const formData = new FormData();
    formData.append("username", editUserData.username);
    formData.append("email", editUserData.email);
    formData.append("role", editUserData.role);
    formData.append("is_staff", editUserData.is_staff);
    formData.append("is_active", editUserData.is_active);

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/user/${editUserId}/`, {
        method: "Put",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
        body: formData, // Send as FormData
      });
  
      const responseData = await response.json();
  
      if (!response.ok) {
        console.error("Error updating user:", responseData);
      } else {
        console.log("User updated successfully:", responseData);
        fetchUsers(token);
        setEditUserId(null);
      }
    } catch (error) {
      console.error("Network error:", error);
    }
  };
  const handlePageClick = ({ selected }) => {
    setCurrentPage(selected);
  };

  const offset = currentPage * imagesPerPage;
  const currentImages = images.slice(offset, offset + imagesPerPage);
  const pageCount = Math.ceil(images.length / imagesPerPage);

  
  return (
    <div className="container mt-4">
      <h1>Admin Dashboard</h1>
           
      <h4>Upload Image</h4>
      <input
        type="file"
        accept="image/*"
        onChange={handleImageChange}
      />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Uploading..." : "Upload"}
      </button>
             
      {/* Images Table */}
      <h2 className="mt-4">Uploaded Images</h2>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Image</th>
            <th>Location</th>
            <th>Latitude</th>
            <th>Longitude</th>
            <th>Distance</th>
            <th>Cost</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {currentImages.map((image) => (
            <tr key={image.id}>
              {editImageId === image.id ? (
                <>
                  <td><Form.Control value={editImageData.location} onChange={(e) => setEditImageData({ ...editImageData, location: e.target.value })} /></td>
                  <td><Form.Control value={editImageData.latitude} onChange={(e) => setEditImageData({ ...editImageData, latitude: e.target.value })} /></td>
                  <td><Form.Control value={editImageData.longitude} onChange={(e) => setEditImageData({ ...editImageData, longitude: e.target.value })} /></td>
                  <td><Form.Control value={editImageData.distance} onChange={(e) => setEditImageData({ ...editImageData, distance: e.target.value })} /></td>
                  <td><Form.Control value={editImageData.cost} onChange={(e) => setEditImageData({ ...editImageData, cost: e.target.value })} /></td>
                  <td><Button variant="success" onClick={handleSaveImage}>Save</Button></td>
                </>
              ) : (
                <>
                  <td><img src={image.image} alt="Image" style={{ width: "100px", height: "100px" }} /></td>
                  <td>{image.location}</td>
                  <td>{image.latitude}</td>
                  <td>{image.longitude}</td>
                  <td>{image.distance}</td>
                  <td>${image.cost}</td>
                  <td>
                    <Button onClick={() => handleEditImage(image)}>Edit</Button></td>
                  <td><Button onClick={() => handleDeleteImage(image.id)}>Delete</Button>
                  </td>
                </>
              )}
            </tr>
          ))}
        </tbody>
      </Table>
      {/* Pagination */}
      <ReactPaginate
            previousLabel={"Previous"}
            nextLabel={"Next"}
            breakLabel={"..."}
            pageCount={pageCount}
            marginPagesDisplayed={2}
            pageRangeDisplayed={5}
            onPageChange={handlePageClick}
            containerClassName={"pagination justify-content-center"}
            pageClassName={"page-item"}
            pageLinkClassName={"page-link"}
            previousClassName={"page-item"}
            previousLinkClassName={"page-link"}
            nextClassName={"page-item"}
            nextLinkClassName={"page-link"}
            breakClassName={"page-item"}
            breakLinkClassName={"page-link"}
            activeClassName={"active"}
        />
        {/* Users Table */}
        <h2 className="mt-4">Users</h2>
        <Table striped bordered hover>
        <thead>
            <tr>
            <th>Username</th>
            <th>Email</th>
            <th>Role</th>
            <th>Is_staff</th>
            <th>Is_active</th>
            {/* <th>Actions</th> */}
            </tr>
        </thead>
        <tbody>
            {users.map((user) => (
            <tr key={user.id}>
                {editUserId === user.id ? (
                <>
                    <td>
                    <Form.Control
                        value={editUserData.username}
                        onChange={(e) =>
                        setEditUserData({ ...editUserData, username: e.target.value })
                        }
                    />
                    </td>
                    <td>
                    <Form.Control
                        value={editUserData.email}
                        onChange={(e) =>
                        setEditUserData({ ...editUserData, email: e.target.value })
                        }
                    />
                    </td>
                    <td>
                    <Form.Control
                        value={editUserData.role}
                        onChange={(e) =>
                        setEditUserData({ ...editUserData, role: e.target.value })
                        }
                    />
                    </td>
                    <td>
                    <Form.Control
                        value={editUserData.is_staff}
                        onChange={(e) =>
                        setEditUserData({ ...editUserData, is_staff: e.target.value })
                        }
                    />
                    </td>
                    <td>
                    <Form.Control
                        value={editUserData.is_active}
                        onChange={(e) =>
                        setEditUserData({ ...editUserData, is_active: e.target.value })
                        }
                    />
                    </td>
                    <td>
                    <Button onClick={handleSaveUser}>Save</Button>
                    </td>
                </>
                ) : (
                <>
                    <td>{user.username}</td>
                    <td>{user.email}</td>
                    <td>{user.role}</td>
                    <td>{user.is_staff ? "true" : "false"}</td>
                    <td>{user.is_active ? "true" : "false"}</td>
                                                            
                </>
                )}
            </tr>
            ))}
        </tbody>
        </Table>
        
        <Button onClick={() => {localStorage.removeItem("user"); navigate("/");}}> Logout </Button>
          
    </div>
  );
};

export default AdminDashboard;
