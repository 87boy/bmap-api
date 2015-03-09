<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Geocoder extends CI_Controller {
    public function __construct() {
        parent::__construct();
        $this->load->model('geocoder_model', 'geocoder');
    }
    public function index() {
        $this->load->view('geocoder.html');
    }
    public function get() {
        $id = $this->input->get();
        //var_dump($id['id']);
        $get = $this->geocoder->get($id['id']);
        var_dump($get);
    }
    public function update_point() {
        $data = $this->input->post();
        //$data = array("status" => "ok");
        //$data = json_encode($data);
        $result = $this->geocoder->update_point($data);
        var_dump($result);
        //return is_array($data);
        //var_dump($data);
    }
    public function insert_poi() {
        $data = $this->input->post();
        $result = $this->geocoder->insert_poi($data);
        var_dump($result);
    }
}