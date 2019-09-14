
//import Link from 'next/link';
import Link from '../ActiveLink';
import {
    MDBNavbar, MDBNavbarBrand, MDBNavbarNav, MDBNavItem, MDBNavbarToggler, MDBCollapse, MDBFormInline,
    MDBDropdown, MDBDropdownToggle, MDBDropdownMenu, MDBDropdownItem, MDBContainer
} from "mdbreact";

const CustomComponent = React.forwardRef(function CustomComponent(props, ref) {
    return (
    <MDBNavItem ref={ref} {...props}>
        <a className="nav-link" >Home</a>
    </MDBNavItem>
    );
});

class Index extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isOpen: false
        };
    }

    toggleCollapse = () => {
        this.setState({ isOpen: !this.state.isOpen });
    }

    

    render() {
        return (
            <div>
            <MDBNavbar color="indigo" dark expand="md">
                <MDBNavbarBrand>
                <strong className="white-text">
                    <center>
                        Post-Storm  
                        <div className="small ">Imagery 🌪️</div>
                    </center>
                </strong>
                </MDBNavbarBrand>
                <MDBNavbarToggler onClick={this.toggleCollapse} />
                <MDBCollapse id="navbarCollapse3" isOpen={this.state.isOpen} navbar>
                    <MDBNavbarNav left>
                        
                        <Link href="/"  activeClassName="active">
                            <CustomComponent/>
                        </Link>

                        <MDBNavItem>
                        <MDBDropdown>
                            <MDBDropdownToggle nav caret>
                                <span className="mr-2">Data Sources</span>
                            </MDBDropdownToggle>
                            <MDBDropdownMenu>
                            
                                <MDBDropdownItem > 
                                <a href="https://storms.ngs.noaa.gov/">NOAA</a>
                                </MDBDropdownItem>
                            
                                <MDBDropdownItem >
                                <a href="https://coastal.er.usgs.gov/hurricanes/tools/oblique.php">USGS</a>
                                </MDBDropdownItem>

                            </MDBDropdownMenu>
                        </MDBDropdown>
                        </MDBNavItem>
                    </MDBNavbarNav>
                </MDBCollapse>
            </MDBNavbar>
          
            {this.props.children}
            </div>
        );
    }
}


const originalError = console.error;

console.error = (...args) => {
if (/Warning.*Function components cannot be given refs/.test(args[0])) {
    return;
}
originalError.call(console, ...args);
};

export default Index;