<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Geocoder_model extends CI_Model {
    public function __construct() {
        parent::__construct();
    }
    public function get($id){
        //return $this->db->get_where('temp_points_copy', array('id' => $id));
        //$res = $this->db->where('id', $id)->limit(1)->get('points');
        $res = $this->db->where('id', $id)->limit(1)->get('temp_points_bd');
        $rst = $res->result();
        if ($rst) {
            $get = json_encode($rst[0]);
            //$get = '1';
            // $result = array();
            // $result['id'] = $get->id;
            // $result['latitude'] = $get->latitude;
            // $result['longitude'] = $get->longitude;
            // $result['blatitude'] = $get->blatitude;
            // $result['blongitude'] = $get->blongitude;
            // $result['address'] = $get->address;
            // $result['business'] = $get->business;
            // $result['uid_list'] = $get->uid_list;
            // $result['title_list'] = $get->title_list;
            // $result['tag_list'] = $get->tag_list;
        } else {
            $get = null;
            //$get = '2';
        }
        //var_dump($get);
        var_dump($get);
    }
    public function update_point($data) {
        $id = $data['id'];
        return $this->db->insert('points', $data);
        //return $this->db->update('temp_points_bd', $data, array('id' => $id));
    }
    public function insert_poi($data) {
        return $this->db->insert('surrounding_pois', $data);
    }
}