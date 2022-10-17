// base url constant
const BASE_URL = "http://127.0.0.1:5000/api";

// handle form submission
const submitNewCupcake = async function(e) {
  e.preventDefault();

  const flavor = $("#flavor").val();
  const rating = $("#rating").val();
  const size = $("#size").val();
  const image = $("#image").val();

  const createdCupcakeRes = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor,
    rating,
    size,
    image
  });

  const createdCupcake = $(generateHtmlForCupcake(createdCupcakeRes.data.cupcake))
  // append to list html element
  $("#list-cupcakes").append(createdCupcake);
  $("#new-cupcake-form").trigger("reset");
};

// function to delete cupcake
const deleteCupcake = async function(e) {
  e.preventDefault();

  const $cupcake = $(e.target).closest('li');
  const cupcakeId = $cupcake.attr("data-cupcake-id");
  
  await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
  $cupcake.remove();
};

// function that creates html for an individual cupcake
const generateHtmlForCupcake = function (cupcake) {
  return  `
  <li data-cupcake-id=${cupcake.id}>
    <p>
    ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
    <button class="delete-btn">X</button>
    </p>
    <img class="cupcake-img" src="${cupcake.image}" alt="${cupcake.flavor} cupcake image">
  </li>`;
};

// function to render cupcakes on page initial load
const renderInitialCupcakes = async function() {
  const res = await axios.get(`${BASE_URL}/cupcakes`);
  res.data.cupcakes.forEach((cupcake) => {
    const newCupcake = $(generateHtmlForCupcake(cupcake));
    $("#list-cupcakes").append(newCupcake);
  })
};

// attach event listeners
$("#list-cupcakes").on("click", ".delete-btn", deleteCupcake);
$("#new-cupcake-form").on("submit", submitNewCupcake);

$(renderInitialCupcakes());