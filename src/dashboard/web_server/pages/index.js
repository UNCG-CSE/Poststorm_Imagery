import Layout from '../src/components/layout'
import Fetch from 'isomorphic-unfetch';
import { MDBBtn, MDBCard, MDBCardBody, MDBCardImage, MDBCardTitle, MDBCardText, MDBCol,MDBContainer } from 'mdbreact';
import public_ip from 'public-ip'

const SAD_FACE =`
https://www.nationwidechildrens.org/-/media/nch/giving/images/on-our-sleeves-1010/icons/icon-teasers/w45084_iconcollectionlandingiconteaserimages_facesad.jpg
`

const Index = (props) => (
    
    <Layout >
        <center>
            <MDBCol className="pt-2">
                <MDBCard style={{ width: "auto" }} className="stylish-color-dark">
                    <MDBCardImage className=" img-fluid pt-4 pb-4 px-2" src={props.data.url || SAD_FACE} alt="The big sad" waves width="768"/>
                    <MDBCardBody >
                        <MDBCardTitle className="white-text h3">{props.data.file_name}</MDBCardTitle>
                        <MDBCardText className="white-text">
                            <b>
                                <u>
                                    Wowe api call
                                </u>
                            </b>
                        </MDBCardText>
                        <MDBCardText className="green-text">       
                            {JSON.stringify(props, null, 4)}   
                        </MDBCardText>
                        <MDBBtn href="register">I dont do anything yet,sorta</MDBBtn>
                    </MDBCardBody>
                </MDBCard>
            </MDBCol>
        </center> 
    </Layout>
    
)

Index.getInitialProps = async function() {
    
    const IP =await public_ip.v4()
    const API_URL='http://'+IP+':4000/images/get_image'
    //Default data incase Fetch fails. 
    let data = {
        file_url:undefined,
        file_name:undefined,
        api_url:API_URL,
   
    }

    await fetch(API_URL).then(async function(received_data) {
        
        data = await received_data.json()
        console.log("Image fetched");
       
    }).catch(function() {
        console.log("Failed to fetch image");
    });
      
    return {
        data:data
    }
}

export default Index;