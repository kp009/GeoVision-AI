import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Table, Button } from "react-bootstrap";
import ReactPaginate from "react-paginate";

const UserDashboard = () => {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(0);
  const imagesPerPage = 5;
  const navigate = useNavigate();

  useEffect(() => {
    const token = JSON.parse(localStorage.getItem("user"))?.token;
    const role = JSON.parse(localStorage.getItem("user"))?.role;
    if (role !== "user") navigate("/");
    if (token) {
      fetchImages(token);
    } else navigate("/login");
  }, [navigate]);

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

  const handlePageClick = ({ selected }) => {
    setCurrentPage(selected);
  };

  const offset = currentPage * imagesPerPage;
  const currentImages = images.slice(offset, offset + imagesPerPage);
  const pageCount = Math.ceil(images.length / imagesPerPage);

  return (
    <div className="container mt-4">
      <h1>User Dashboard</h1>

      {/* Images Table */}
      <h4 className="mt-4">Uploaded Images</h4>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Image</th>
            <th>Location</th>
            <th>Latitude</th>
            <th>Longitude</th>
            <th>Distance</th>
            <th>Cost</th>
          </tr>
        </thead>
        <tbody>
          {currentImages.map((image) => (
            <tr key={image.id}>
              <td><img src={image.image} alt="Image" style={{ width: "100px", height: "100px" }} /></td>
              <td>{image.location}</td>
              <td>{image.latitude}</td>
              <td>{image.longitude}</td>
              <td>{image.distance}</td>
              <td>${image.cost}</td>
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

      <Button onClick={() => { localStorage.removeItem("user"); navigate("/"); }}>
        Logout
      </Button>
    </div>
  );
};

export default UserDashboard;
